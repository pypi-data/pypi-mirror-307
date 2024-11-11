from enum import Enum, auto


class StoppingEvent(Enum):
    PERIAPSIS = auto()
    APOAPSIS = auto()
