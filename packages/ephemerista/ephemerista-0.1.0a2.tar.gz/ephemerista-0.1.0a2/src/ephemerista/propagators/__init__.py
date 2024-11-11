import abc
from typing import overload

from ephemerista import BaseModel
from ephemerista.coords.trajectories import Trajectory
from ephemerista.coords.twobody import Cartesian
from ephemerista.propagators.events import StoppingEvent
from ephemerista.time import Time


class Propagator(BaseModel, abc.ABC):
    @overload
    @abc.abstractmethod
    def propagate(self, time: Time) -> Cartesian: ...

    @overload
    @abc.abstractmethod
    def propagate(self, time: list[Time]) -> Trajectory: ...

    @overload
    @abc.abstractmethod
    def propagate(self, time: Time, stop_conds: list[StoppingEvent] | None = None) -> Cartesian: ...

    @overload
    @abc.abstractmethod
    def propagate(self, time: list[Time], stop_conds: list[StoppingEvent] | None = None) -> Trajectory: ...

    @abc.abstractmethod
    def propagate(
        self,
        time: Time | list[Time],
        stop_conds: list[StoppingEvent] | None = None,
    ) -> Cartesian | Trajectory:
        pass
