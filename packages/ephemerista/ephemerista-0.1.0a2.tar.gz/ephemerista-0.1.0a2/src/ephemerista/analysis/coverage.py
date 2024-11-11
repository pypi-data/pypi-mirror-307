from pathlib import Path

import antimeridian
import geopandas as gpd
import healpy as hp
import numpy as np
import pandas as pd
import plotly.express as px
import pydantic_numpy.typing as pnd
from geojson_pydantic import Feature, FeatureCollection
from geojson_pydantic import Polygon as PolygonPydantic
from matplotlib.axes import Axes
from plotly.graph_objs import Figure
from pydantic import Field
from shapely import MultiPolygon, Polygon

from ephemerista import BaseModel
from ephemerista.analysis import Analysis
from ephemerista.analysis.visibility import Visibility, VisibilityResults
from ephemerista.assets import GroundPoint, Spacecraft
from ephemerista.scenarios import Ensemble, Scenario
from ephemerista.time import Time

PolygonFeature = Feature[PolygonPydantic, dict]
PolygonFeatureCollection = FeatureCollection[PolygonFeature]


def polygonize_earth(n_cells_min: int) -> list[PolygonFeature]:
    """
    Polygonizes the Earth using healpix and based on the given number of cells
    """
    nside = int(np.sqrt(n_cells_min / 12.0)) + 1
    n_pix = hp.nside2npix(nside)
    ipix = np.arange(n_pix)
    nested = False

    feature_list = []
    geometry = []
    for i in ipix:
        bound_vectors = hp.boundaries(nside, i, nest=nested)
        lon_array, lat_array = hp.vec2ang(bound_vectors.T, lonlat=True)
        polygon = Polygon(np.vstack((lon_array, lat_array)).T)
        poly_or_multipoly = antimeridian.fix_polygon(polygon)
        geometry.append(poly_or_multipoly)
        if isinstance(
            poly_or_multipoly, MultiPolygon
        ):  # antimeridian sometimes has to split a polygon and returns a MultiPolygon instead
            for poly in poly_or_multipoly.geoms:
                feature_list.append(PolygonFeature(geometry=poly, properties={}, type="Feature"))
        else:
            feature_list.append(PolygonFeature(geometry=poly_or_multipoly, properties={}, type="Feature"))

    return feature_list


def load_geojson_multipolygon(filename: Path | str) -> list[PolygonFeature]:
    with open(filename) as f:
        json_str = f.read()

    model = PolygonFeatureCollection.model_validate_json(json_str)
    return model.features


class CoverageResults(BaseModel):
    polygons: list[PolygonFeature] = Field()
    coverage_percentages: pnd.Np1DArrayFp32

    def plot_mpl(self, legend: bool = True, **kwargs) -> Axes:  # noqa: FBT001, FBT002
        geo_df = self.to_geodataframe()
        ax = geo_df.plot(
            column="coverage_percent", legend_kwds={"label": "Coverage percentage [0-1]"}, legend=legend, **kwargs
        )
        ax.set_ylabel("Longitude [°]")
        ax.set_xlabel("Latitude [°]")
        return ax

    def plot_plotly(
        self, mapbox_style: str = "open-street-map", zoom: int = 0, opacity: float = 0.7, **kwargs
    ) -> Figure:
        geo_df = self.to_geodataframe()
        fig = px.choropleth_mapbox(
            geo_df,
            geojson=geo_df.geometry,
            locations=geo_df.index,
            color="coverage_percent",
            mapbox_style=mapbox_style,
            zoom=zoom,
            opacity=opacity,
            **kwargs,
        )
        return fig

    def to_geodataframe(self) -> gpd.GeoDataFrame:
        gdf = gpd.GeoDataFrame.from_features(self.polygons)
        gdf["coverage_percent"] = self.coverage_percentages
        return gdf

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(data=self.coverage_percentages, columns=["cov_percent"])


class Coverage(Analysis[CoverageResults]):
    """
    The coverage is computed by computing all passes of the spacecraft over all points of the exterior of each polygon,
      i.e. the visibility from 0° elevation.
    Doing that for all points of the exterior of each polygon is computationally intensive, but that allows to do an
      average of the coverage on the polygon. Besides, when the GroundPoints are created in scenarios.py,
      shared points between adjacent polygons are merged to avoid duplicate computations.
    For instance for a polygon's exterior composed of 4 points, if two points have spacecraft visibility for a total
      duration of 340 seconds, and the two other points for 360 seconds, then the average visibility duration of this
      polygon will be 350 seconds.
    """

    scenario: Scenario
    start_time: Time | None = Field(default=None)
    end_time: Time | None = Field(default=None)

    def analyze(
        self,
        ensemble: Ensemble | None = None,
        visibility: VisibilityResults | None = None,
    ) -> CoverageResults:
        if not ensemble:
            ensemble = self.scenario.propagate()

        if not visibility:
            visibility = Visibility(scenario=self.scenario, start_time=self.start_time, end_time=self.end_time).analyze(
                ensemble
            )

        ts = self.scenario.start_time
        te = self.scenario.end_time
        scenario_duration = (te - ts).to_decimal_seconds()

        # initialize result struct
        total_covered_time = np.zeros(len(self.scenario.areas_of_interest))

        ground_point_intervals_dict = {
            asset.asset_id: [] for asset in self.scenario.assets if isinstance(asset.model, GroundPoint)
        }

        for target_id, observers in visibility.passes.items():
            target = self.scenario[target_id]
            if not isinstance(target.model, Spacecraft):
                continue

            for observer_id, passes in observers.items():
                observer = self.scenario[observer_id]
                if not isinstance(observer.model, GroundPoint):
                    continue

                for gs_pass in passes:
                    t0 = gs_pass.window.start
                    t0_rel = (t0 - ts).to_decimal_seconds()  # TODO: try to do the same computation with Time objects
                    t1 = gs_pass.window.stop
                    t1_rel = (t1 - ts).to_decimal_seconds()
                    ground_point_intervals_dict[observer_id].append([t0_rel, t1_rel])

        for observer_id, intervals in ground_point_intervals_dict.items():
            # Sorting and merging time intervals, based on https://stackoverflow.com/a/65282946

            intervals_df = pd.DataFrame.from_records(intervals, columns=["START", "FINISH"])

            intervals_df.sort_values("START", inplace=True)
            intervals_df["group"] = (intervals_df["START"] > intervals_df["FINISH"].shift().cummax()).cumsum()
            merged_intervals_df = intervals_df.groupby("group").agg({"START": "min", "FINISH": "max"})

            merged_intervals_df["duration"] = merged_intervals_df["FINISH"] - merged_intervals_df["START"]
            total_duration_ground_point = merged_intervals_df["duration"].sum()

            ground_point = self.scenario[observer_id].model
            for polygon_id in ground_point.polygon_ids:
                n_polygon_points = self.scenario.areas_of_interest[polygon_id].properties["n_exterior_points"]
                total_covered_time[polygon_id] += total_duration_ground_point / n_polygon_points

        return CoverageResults(
            polygons=self.scenario.areas_of_interest, coverage_percentages=total_covered_time / scenario_duration
        )
