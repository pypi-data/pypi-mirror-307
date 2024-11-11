import abc
import math
from typing import Literal, Self

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, PrivateAttr, computed_field

from ephemerista import bodies
from ephemerista.assets import Asset, Spacecraft
from ephemerista.constellation.plane import Plane
from ephemerista.coords.twobody import DEFAULT_ORIGIN, Keplerian, Origin
from ephemerista.propagators.orekit import OrekitPropagator
from ephemerista.scenarios import Scenario
from ephemerista.time import Time

DEFAULT_PLANET: Literal["earth"] = "earth"


class AbstractConstellation(BaseModel, abc.ABC):
    nsats: int = Field(gt=0, description="Number of satellites in the constellation")
    nplanes: int = Field(gt=0, description="Number of orbital planes in the constellation")
    semi_major_axis: float = Field(gt=0, description="Semi major axis, in km")
    inclination: float = Field(ge=0, description="Inclination, in degrees")
    eccentricity: float = Field(ge=0, description="Eccentricity")
    periapsis_argument: float = Field(ge=0, description="Argument of Perigee, in degrees")
    phasing: int = Field(default=0, ge=0, description="Phasing between satellites in adjacent planes")
    name: str = Field(default="My Constellation", description="Name of the Constellation")
    origin: Origin = Field(
        default=DEFAULT_ORIGIN,
        discriminator=bodies.DISCRIMINATOR,
        description="Origin of the coordinate system",
    )
    time: Time = Field(description="Epoch of the constellation")

    # Define private attributes for easier computation
    _sats_per_plane: int = PrivateAttr()
    _semi_major_axis_m: float = PrivateAttr()
    _inclination_radians: float = PrivateAttr()
    _argument_of_periapsis_radians: float = PrivateAttr()

    #  Define private attributes for future gets
    _planes: dict[int, Plane] = PrivateAttr()
    _satellites: list[Keplerian] = PrivateAttr()

    def model_post_init(self, __context):
        # Initialise private attributes in computationally efficient units
        self._semi_major_axis_m = self.semi_major_axis / 1000.0
        self._inclination_radians = np.radians(self.inclination)
        self._argument_of_periapsis_radians = np.radians(self.periapsis_argument)

        if self.nsats % self.nplanes != 0:
            msg = "The number of satellites per plane must be a multiple of the number of planes for a constellation."
            raise ValueError(msg)
        self._sats_per_plane = self.nsats // self.nplanes

        if self.phasing >= self.nplanes:
            msg = "Phasing must be lower than the number of planes"
            raise ValueError(msg)

        # Initialise private attributes for future gets
        self._planes = {}
        self._satellites = []

        valid, reason = Keplerian.is_physical(
            semi_major_axis=self.semi_major_axis,
            eccentricity=self.eccentricity,
            inclination=self.inclination,
            periapsis_argument=self.periapsis_argument,
            origin=self.origin,
        )
        if not valid:
            error_message = f"The constellation is not physical: {reason}"
            raise ValueError(error_message)

    def __eq__(self, other: Self) -> bool:
        rules = [
            self.nsats == other.nsats,
            self.nplanes == other.nplanes,
            math.isclose(self.semi_major_axis, other.semi_major_axis, rel_tol=1e-9),
            math.isclose(self.inclination, other.inclination, rel_tol=1e-9),
            math.isclose(self.eccentricity, other.eccentricity, rel_tol=1e-9),
            math.isclose(self.semi_major_axis, other.semi_major_axis, rel_tol=1e-9),
            self.name == other.name,
            self.origin == other.origin,
            self.time == other.time,
            len(self.satellites) == len(other.satellites),
        ]
        rules += [self.satellites[i] == other.satellites[i] for i in range(0, len(self.satellites))]
        return all(rules)

    @property
    def sma(self):
        """Returns the semi-major axis, in km."""
        return self.semi_major_axis

    @property
    def ecc(self):
        """Returns the eccentricity."""
        return self.eccentricity

    @property
    def inc(self):
        """Returns the inclination."""
        return self.inclination

    @property
    def aop(self):
        """Returns the argument of periapsis."""
        return self.periapsis_argument

    @property
    def number_satellites(self):
        """Returns the number of satellites."""
        return self.nsats

    @property
    def sma_m(self):
        return self._semi_major_axis_m

    @property
    def planes(self):
        """Method to return the planes to the user, with results cached for future gets."""
        if not hasattr(self, "_planes"):
            self._planes = self.define_planes()
        return self._planes

    @computed_field
    @property
    def satellites(self) -> list[Keplerian]:
        """Method to return the satellites to the user, with results cached for future gets."""
        if not hasattr(self, "_satellites"):
            self._satellites = self.define_satellites()
        return self._satellites

    @abc.abstractmethod
    def define_planes(self) -> dict[int, Plane]:
        """Returns a list of Plane objects that define the constellation."""
        pass

    @abc.abstractmethod
    def define_satellites(self) -> list[Keplerian]:
        """Returns a list of Keplerian objects that define the constellation's satellites."""
        pass

    @abc.abstractmethod
    def to_dataframe(self) -> pd.DataFrame:
        """Generates a dataframe of the Keplarian elements of each plane in the constellation.

        Returns:
            pd.DataFrame: Dataframe of Keplarian elements
        """
        pass

    def gen_scenario(self, scenario_templ: Scenario, prop_templ: OrekitPropagator) -> Scenario:
        """
        Adds satellites to a scenario template using a propagator template
        :return: a copy of the scenario template with additional Spacecraft Assets based on the constellation geometry
        """
        sc_list: list[Asset] = []
        for state_init in self.satellites:
            prop = prop_templ.model_copy(update={"state_init": state_init})
            sc_list.append(Asset(model=Spacecraft(type="spacecraft", propagator=prop), name=state_init.satellite_name))
        return scenario_templ.model_copy(update={"assets": scenario_templ.assets + sc_list})


class AbstractWalker(AbstractConstellation, abc.ABC):
    """A Walker Star or Delta Constellation."""

    _raan_spacing: float = PrivateAttr()
    _anomaly_spacing: float = PrivateAttr()
    _anomaly_phasing: float = PrivateAttr()  # Additional anomaly offset between adjacent planes

    def model_post_init(self, __context):
        super().model_post_init(__context)

        self._anomaly_spacing = 360 / self._sats_per_plane
        self._planes = self.define_planes()
        self._satellites = self.define_satellites()

    def define_planes(self) -> dict[int, Plane]:
        """Using the user defined constellation inputs (number of satellites, number of planes, keplarian elements etc.)
        generates Plane objects to fully define the constellation."""
        planes = {}

        for p in range(self.nplanes):
            ascending_node = p * self._raan_spacing

            # Initialise planes equally spaced in raan
            planes.update(
                {
                    p + 1: Plane(
                        plane_id=p + 1,
                        inclination=self.inclination,
                        ascending_node=ascending_node,
                        semi_major_axis=self.semi_major_axis,
                        eccentricity=self.eccentricity,
                        periapsis_argument=self.periapsis_argument,
                        number_of_satellites=self._sats_per_plane,
                        primary_body=self.origin,
                    )
                }
            )
        return planes

    def define_satellites(self) -> list[Keplerian]:
        """Using the user defined constellation inputs (number of satellites, number of planes,
        phasing, keplerian elements etc.) generates Keplerian objects
        to fully define the constellation.

        Returns
        -------
        list[Keplerian]
            list of Keplerian objects
        """
        satellites = []

        for p in range(self.nplanes):
            ascending_node = p * self._raan_spacing

            for j in range(self._sats_per_plane):
                arg_latitude = j * self._anomaly_spacing + 2 * p * self._anomaly_phasing
                while arg_latitude > 180.0:  # noqa: PLR2004
                    arg_latitude -= 360.0

                satellites.append(
                    Keplerian.from_elements(
                        time=self.time,
                        semi_major_axis=self.semi_major_axis,
                        eccentricity=self.eccentricity,
                        inclination=self.inclination,
                        periapsis_argument=self.periapsis_argument,
                        ascending_node=ascending_node,
                        anomaly=arg_latitude,  # Spread satellites evenly in argument of latitude, starting at 0 deg.
                        # This is satellite number (j), divided by the total satellites per plane, multiplied by 2pi
                        origin=self.origin,
                        satellite_name=f"Sat_P{p+1}_{j}",
                    )
                )

        return satellites

    def to_dataframe(self, data: str = "planes") -> pd.DataFrame:
        """Returns a dataframe of the Keplarian elements of each plane in the constellation, or
        the satellites in each plane,depending on the input

        Parameters
        ----------
        data : str, optional
            Flag to return plane or satellite data. Defaults to "planes"

        Returns
        -------
        pd.DataFrame
            Dataframe of Keplarian elements of each constellation,
            or the satellites in each plane, depending on the input
        """
        if data.lower() == "planes":
            return pd.concat([pd.DataFrame.from_records([p.elements]) for p in self.planes.values()], ignore_index=True)
        if data.lower() == "satellites":
            # Flatten values into a single list
            return pd.concat([sc.to_dataframe() for sc in self.satellites], ignore_index=True)
        else:
            msg = "Data requested should be 'planes' or 'satellites'"
            raise ValueError(msg)


class WalkerStar(AbstractWalker):
    constellation_type: Literal["walker_star"] = Field(
        default="walker_star", frozen=True, alias="type", description="The type of constellation"
    )

    def model_post_init(self, __context):
        self._raan_spacing = (360 / 2) / self.nplanes
        self._anomaly_phasing = (
            self.phasing * 180 / self.nsats
        )  # https://uk.mathworks.com/help/aerotbx/ug/satellitescenario.walkerstar.html#mw_fb3f83e6-67c5-4ff5-b6f8-c4a4e65f6a78

        # Here the super is called at the end because AbstractWalker's constructor needs to know the _raan_spacing value
        super().model_post_init(__context)


class WalkerDelta(AbstractWalker):
    constellation_type: Literal["walker_delta"] = Field(
        default="walker_delta", frozen=True, alias="type", description="The type of constellation"
    )

    def model_post_init(self, __context):
        self._raan_spacing = 360 / self.nplanes
        self._anomaly_phasing = (
            self.phasing * 180 / self.nsats
        )  # https://de.mathworks.com/help/aerotbx/ug/satellitescenario.walkerdelta.html#mw_badf1acd-4f40-4ad6-987e-c7d35ae2368c

        # Here the super is called at the end because AbstractWalker's constructor needs to know the _raan_spacing value
        super().model_post_init(__context)


type Constellation = WalkerStar | WalkerDelta
