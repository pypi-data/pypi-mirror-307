from pathlib import Path
from typing import Self
from uuid import uuid4

import geopandas as gpd
import pyproj
from geojson_pydantic import Feature, Point, Polygon  # type: ignore
from pydantic import UUID4, Field
from shapely import Point as ShapelyPoint
from shapely.ops import transform

from ephemerista import BaseModel, bodies
from ephemerista.assets import Asset, AssetKey, GroundPoint, asset_id
from ephemerista.comms.channels import Channel
from ephemerista.coords.trajectories import Trajectory
from ephemerista.coords.twobody import DEFAULT_FRAME, DEFAULT_ORIGIN, Origin
from ephemerista.frames import ReferenceFrame
from ephemerista.time import Time


class Ensemble(BaseModel):
    trajectories: dict[UUID4, Trajectory]

    def __getitem__(self, asset: AssetKey) -> Trajectory:
        return self.get(asset)

    def get(self, asset: AssetKey) -> Trajectory:
        return self.trajectories[asset_id(asset)]


class Scenario(BaseModel):
    scenario_id: UUID4 = Field(alias="id", default_factory=uuid4)
    name: str = Field(description="The name of the scenario", default="Scenario")
    start_time: Time
    end_time: Time
    time_step: float = Field(default=60)
    origin: Origin = Field(
        default=DEFAULT_ORIGIN,
        discriminator=bodies.DISCRIMINATOR,
        description="Origin of the coordinate system",
    )
    frame: ReferenceFrame = Field(default=DEFAULT_FRAME, description="Reference frame of the coordinate system")
    assets: list[Asset] = Field(default=[])
    channels: list[Channel] = Field(default=[])
    points_of_interest: list[Feature[Point, dict]] = Field(default=[])
    areas_of_interest: list[Feature[Polygon, dict]] = Field(default=[])

    def __init__(self, **data):
        super().__init__(**data)
        self._gen_points_from_aoi()

    def _gen_points_from_aoi(self):
        """
        Add GroundPoint Assets to the propagator, representing the exterior points of the polygons
        defined by the scenario's areas_of_interest.
        In a grid represented by adjacent polygons, points are shared between multiple polygons,
        therefore to avoid duplicate ground points (and thus extra computations), we do the following:
          - identify which points are shared between polygons
          - only keep one point but keep track of all polygons this point belongs to
        """
        delta_m_max = 1.0  # distance threshold in meters to decide if a point belongs to a polygon's exterior

        wgs84 = pyproj.CRS("EPSG:4326")
        mercator = pyproj.CRS("EPSG:3857")
        project = pyproj.Transformer.from_crs(wgs84, mercator, always_xy=True).transform

        gdf = gpd.GeoDataFrame(columns=["geometry", "ground_point"], crs="EPSG:3857")
        u_point_id = 0

        for polygon_id in range(0, len(self.areas_of_interest)):
            polygon = self.areas_of_interest[polygon_id]
            geometry = polygon.geometry
            exterior = geometry.exterior
            self.areas_of_interest[polygon_id].properties["polygon_id"] = polygon_id
            n_points = len(exterior) - 1  # Omitting the last point which is the same as the first point
            self.areas_of_interest[polygon_id].properties["n_exterior_points"] = n_points

            for point_id in range(0, n_points):
                point = exterior[point_id]
                shapely_point = transform(project, ShapelyPoint(point.longitude, point.latitude))

                u_point_id_match = 0
                within_distance = False
                if len(gdf) > 0:
                    distances = gdf.distance(shapely_point)
                    u_point_id_match = distances.idxmin()
                    within_distance = distances[u_point_id_match] < delta_m_max

                if within_distance:
                    # we found an existing polygon point within distance threshold
                    gdf.loc[u_point_id_match, "ground_point"].polygon_ids.append(polygon_id)
                else:
                    gdf.loc[u_point_id] = [
                        shapely_point,
                        GroundPoint.from_lla(
                            latitude=point.latitude, longitude=point.longitude, polygon_ids=[polygon_id]
                        ),
                    ]
                    u_point_id += 1
        for polygon_root_id, points_data in gdf.iterrows():
            self.assets.append(
                Asset(
                    model=points_data["ground_point"],
                    name=f"polygon_{polygon_root_id}",
                )
            )

    @classmethod
    def load_from_file(cls, path: Path | str) -> Self:
        if isinstance(path, str):
            path = Path(path)
        json = path.read_text()
        return cls.model_validate_json(json)

    def get_asset(self, asset: AssetKey | str) -> Asset:
        if isinstance(asset, str):
            return next(a for a in self.assets if a.name == asset)
        return next(a for a in self.assets if a.asset_id == asset_id(asset))

    def __getitem__(self, asset: AssetKey | str) -> Asset:
        return self.get_asset(asset)

    def channel_by_id(self, channel_id: UUID4) -> Channel:
        return next(c for c in self.channels if c.channel_id == channel_id)

    def times(self) -> list[Time]:
        return self.start_time.trange(self.end_time, self.time_step)

    def propagate(self) -> Ensemble:
        trajectories = {asset.asset_id: asset.model.propagate(self.times()) for asset in self.assets}
        return Ensemble(trajectories=trajectories)
