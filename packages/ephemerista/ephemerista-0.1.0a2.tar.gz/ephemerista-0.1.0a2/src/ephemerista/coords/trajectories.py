from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Literal, Self

import lox_space as lox
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pydantic_numpy.typing as pnd
from pydantic import Field, PrivateAttr

from ephemerista import BaseModel, bodies
from ephemerista.coords.twobody import DEFAULT_FRAME, DEFAULT_ORIGIN, Cartesian, Origin
from ephemerista.frames import ReferenceFrame
from ephemerista.time import Scale, Time


class Event(BaseModel):
    time: Time
    crossing: Literal["up", "down"]

    @classmethod
    def _from_lox(cls, event: lox.Event) -> Self:
        return cls(time=Time._from_lox(event.time()), crossing=event.crossing().lower())


class Trajectory(BaseModel):
    """
    Generic trajectory model
    """

    start_time: Time
    origin: Origin = Field(
        default=DEFAULT_ORIGIN,
        discriminator=bodies.DISCRIMINATOR,
        description="Origin of the coordinate system",
    )
    frame: ReferenceFrame = Field(default=DEFAULT_FRAME, description="Reference frame of the coordinate system")
    states: pnd.Np2DArrayFp64
    name: str | None = Field(default=None, description="Name of the asset")
    _trajectory: lox.Trajectory = PrivateAttr()

    def __init__(self, trajectory: lox.Trajectory | None = None, **data):
        super().__init__(**data)

        if not trajectory:
            self._trajectory = lox.Trajectory.from_numpy(
                self.start_time._time, self.states, self.origin._body, self.frame._frame
            )
        else:
            self._trajectory = trajectory

    @classmethod
    def _from_lox(cls, trajectory: lox.Trajectory) -> Self:
        states = trajectory.to_numpy()
        origin = bodies._from_lox(trajectory.origin())
        frame = ReferenceFrame._from_lox(trajectory.reference_frame())
        start_time = Time._from_lox(trajectory.states()[0].time())
        return cls(trajectory=trajectory, states=states, origin=origin, frame=frame, start_time=start_time)

    @classmethod
    def from_csv(
        cls,
        path: str | Path,
        scale: Scale | Literal["UTC"] = "TAI",
        frame: ReferenceFrame = DEFAULT_FRAME,
        origin: Origin = DEFAULT_ORIGIN,
        **kwargs,
    ) -> Self:
        """
        Reads a trajectory from a CSV file.
        """
        df = pd.read_csv(path, delimiter=",", **kwargs)
        states = np.empty((len(df), 7), dtype=np.float64)
        if scale == "UTC":
            start_time = Time.from_utc(df.iloc[0, 0])
        else:
            start_time = Time.from_iso(scale, df.iloc[0, 0])
        for i, row in df.iterrows():
            iso, *data = row.array
            if scale == "UTC":
                time = Time.from_utc(iso)
            else:
                time = Time.from_iso(scale, iso)
            states[i, 0] = float(time - start_time)
            states[i, 1:] = data

        return cls(states=states, start_time=start_time, frame=frame, origin=origin)

    @property
    def cartesian_states(self) -> list[Cartesian]:
        """
        List of states in the trajectory
        """
        return [Cartesian._from_lox(s) for s in self._trajectory.states()]

    @property
    def times(self) -> list[Time]:
        """
        List of times in the trajectory
        """
        return [s.time for s in self.cartesian_states]

    @property
    def datetimes(self) -> list[datetime]:
        return [t.datetime for t in self.times]

    def to_csv(self, path: str, **kwargs):
        """
        Writes the trajectory to a CSV file.
        """
        df = pd.DataFrame(
            (
                (state.time.to_utc(), state.x, state.y, state.z, state.vx, state.vy, state.vz)
                for state in self.cartesian_states
            ),
            columns=["utc", "x", "y", "z", "vx", "vy", "vz"],
        )
        df.to_csv(path, index=False, **kwargs)

    def interpolate(self, time: Time) -> Cartesian:
        """
        Interpolates the state of the trajectory at a given time.

        Parameters
        ----------
        time: Time
            Time at which to interpolate the state

        Returns
        -------
        Cartesian
            Interpolated state of the trajectory
        """
        return Cartesian._from_lox(self._trajectory.interpolate(time._time))

    def plot_3d(self) -> go.Scatter3d:
        scatter = go.Scatter3d(
            x=self.states[:, 1],
            y=self.states[:, 2],
            z=self.states[:, 3],
            mode="lines",
            name="Trajectory",
            hovertext=[t.to_utc() for t in self.times],
        )
        return scatter

    def find_events(self, func: Callable[[Cartesian], float]) -> list[Event]:
        events = self._trajectory.find_events(lambda s: func(Cartesian._from_lox(s)))
        return [Event._from_lox(e) for e in events]
