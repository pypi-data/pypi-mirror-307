import math
from typing import overload

import numpy as np
from numpy.typing import ArrayLike

BOLTZMANN_CONSTANT: float = 1.38064852e-23  # J/K
ROOM_TEMPERATURE = 290  # K
SPEED_OF_LIGHT_VACUUM: float = 2.99792458e8  # m/s


def wavelength(frequency: float) -> float:
    return SPEED_OF_LIGHT_VACUUM / frequency


@overload
def to_db(val: float) -> float: ...


@overload
def to_db(val: ArrayLike) -> ArrayLike: ...


def to_db(val: ArrayLike | float) -> ArrayLike | float:
    return 10 * np.log10(val)


def from_db(val: float) -> float:
    return 10 ** (val / 10)


def free_space_path_loss(distance: float, frequency: float) -> float:
    return to_db((4 * math.pi * distance * 1e3 / wavelength(frequency)) ** 2)
