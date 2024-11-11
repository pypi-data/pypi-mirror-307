import uuid
from typing import Literal, Self, overload

import lox_space as lox
import numpy as np
from pydantic import UUID4, Field, PrivateAttr

from ephemerista import BaseModel, get_provider
from ephemerista.angles import Angle, Latitude, Longitude
from ephemerista.bodies import Planet
from ephemerista.comms.systems import CommunicationSystem
from ephemerista.coords.trajectories import Trajectory
from ephemerista.coords.twobody import Cartesian
from ephemerista.math import angle_between
from ephemerista.propagators.orekit.numerical import NumericalPropagator
from ephemerista.propagators.orekit.semianalytical import SemiAnalyticalPropagator
from ephemerista.propagators.sgp4 import SGP4
from ephemerista.propagators.trajectory import TrajectoryPropagator
from ephemerista.time import Time

type Propagator = TrajectoryPropagator | SGP4 | NumericalPropagator | SemiAnalyticalPropagator


class Spacecraft(BaseModel):
    asset_type: Literal["spacecraft"] = Field(default="spacecraft", alias="type", repr=False, frozen=True)
    propagator: Propagator = Field(discriminator="propagator_type")

    @overload
    def propagate(self, time: Time) -> Cartesian: ...

    @overload
    def propagate(self, time: list[Time]) -> Trajectory: ...

    def propagate(self, time: Time | list[Time]) -> Cartesian | Trajectory:
        return self.propagator.propagate(time)

    def off_boresight_angle(self, sc: Cartesian, other: Cartesian, comms: CommunicationSystem) -> float:
        r = other.position - sc.position
        ru = r / np.linalg.norm(r)
        rot = sc.rotation_lvlh()

        angle = angle_between(rot @ ru, comms.antenna.boresight_array) - comms.antenna.field_of_regard.radians
        return max(0, angle)


class Observables(BaseModel):
    azimuth: Angle
    elevation: Angle
    rng: float
    rng_rate: float

    @classmethod
    def _from_lox(cls, obs: lox.Observables) -> Self:
        return cls(
            azimuth=Angle.from_radians(obs.azimuth()),
            elevation=Angle.from_radians(obs.elevation()),
            rng=obs.range(),
            rng_rate=obs.range_rate(),
        )


class GroundStation(BaseModel):
    asset_type: Literal["groundstation"] = Field(default="groundstation", alias="type", repr=False, frozen=True)
    body: Planet = Field(default=Planet(name="Earth"))
    longitude: Longitude
    latitude: Latitude
    altitude: float = Field(default=0)
    minimum_elevation: Angle = Field(default=Angle.from_degrees(0))
    _location: lox.GroundLocation = PrivateAttr()

    def __init__(self, location: lox.GroundLocation | None = None, **data):
        super().__init__(**data)

        if not location:
            self._location = lox.GroundLocation(
                self.body._body,
                self.longitude.radians,
                self.latitude.radians,
                self.altitude,
            )
        else:
            self._location = location

    @classmethod
    def from_lla(cls, longitude: float, latitude: float, **data) -> Self:
        return cls(
            longitude=Longitude.from_degrees(longitude),
            latitude=Latitude.from_degrees(latitude),
            **data,
        )

    def observables(self, target: Cartesian) -> Observables:
        obs = self._location.observables(target._cartesian)
        return Observables._from_lox(obs)

    @overload
    def propagate(self, time: Time) -> Cartesian: ...

    @overload
    def propagate(self, time: list[Time]) -> Trajectory: ...

    def propagate(self, time: Time | list[Time]) -> Cartesian | Trajectory:
        provider = get_provider()
        propagator = lox.GroundPropagator(self._location, provider)
        if isinstance(time, Time):
            return Cartesian._from_lox(propagator.propagate(time._time))
        else:
            return Trajectory._from_lox(propagator.propagate([time._time for time in time]))

    def off_boresight_angle(self, elevation: float, comms: CommunicationSystem) -> float:
        return max(0, elevation - comms.antenna.field_of_regard.degrees)

    def rotation_to_topocentric(self) -> np.ndarray:
        return self._location.rotation_to_topocentric()


class GroundPoint(GroundStation):
    asset_type: Literal["groundpoint"] = Field(default="groundpoint", alias="type", repr=False, frozen=True)
    polygon_ids: list[int] = Field()  # IDs of the polygon this point belongs to. Can be multiple in case of a grid


class Asset(BaseModel):
    asset_id: UUID4 = Field(alias="id", default_factory=uuid.uuid4)
    name: str = Field(description="The name of the asset", default="Asset")
    model: Spacecraft | GroundStation | GroundPoint = Field(discriminator="asset_type")
    comms: list[CommunicationSystem] = Field(default=[])

    def comms_by_channel_id(self, channel_id: UUID4) -> CommunicationSystem:
        return next(c for c in self.comms if channel_id in c.channels)


type AssetKey = UUID4 | Asset


def asset_id(asset: AssetKey) -> UUID4:
    if isinstance(asset, Asset):
        return asset.asset_id
    elif isinstance(asset, uuid.UUID):
        return asset
