from __future__ import annotations

import abc
from typing import Literal

from pydantic import Field

from ephemerista import BaseModel
from ephemerista.assets import GroundStation
from ephemerista.coords.trajectories import Event, Trajectory
from ephemerista.coords.twobody import Cartesian


class EventDetector(abc.ABC):
    @abc.abstractmethod
    def callback(self, s: Cartesian) -> float:
        raise NotImplementedError()

    def filtr(self, events: list[Event]) -> list[Event]:
        return events

    def detect(self, trajectory: Trajectory) -> list[Event]:
        return self.filtr(trajectory.find_events(lambda s: self.callback(s)))


class ApsisDetector(BaseModel, EventDetector):
    apsis: Literal["periapsis", "apoapsis"] | None = Field(default=None)

    def callback(self, s: Cartesian) -> float:
        return s.position @ s.velocity  # type: ignore

    def filtr(self, events: list[Event]) -> list[Event]:
        if self.apsis == "periapsis":
            return [e for e in events if e.crossing == "up"]
        elif self.apsis == "apoapsis":
            return [e for e in events if e.crossing == "down"]
        return events


class ElevationDetector(BaseModel, EventDetector):
    ground_station: GroundStation

    def callback(self, s: Cartesian) -> float:
        return self.ground_station.observables(s).elevation.radians - self.ground_station.minimum_elevation.radians
