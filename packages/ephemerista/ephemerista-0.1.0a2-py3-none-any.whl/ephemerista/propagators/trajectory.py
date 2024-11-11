from typing import Literal

import lox_space as lox
from pydantic import Field

from ephemerista.coords.trajectories import Trajectory
from ephemerista.coords.twobody import Cartesian
from ephemerista.propagators import Propagator
from ephemerista.time import Time


class TrajectoryPropagator(Propagator):
    propagator_type: Literal["trajectory"] = Field(
        default="trajectory", frozen=True, repr=False, alias="type", description="The type of the propagator"
    )
    trajectory: Trajectory

    def propagate(self, time: Time | list[Time]) -> Cartesian | Trajectory:
        if isinstance(time, Time):
            return self.trajectory.interpolate(time)
        else:
            states = [self.trajectory._trajectory.interpolate(t._time) for t in time]
            return Trajectory._from_lox(lox.Trajectory(states))
