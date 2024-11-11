import abc
from typing import Literal

import numpy as np
from pydantic import Field
from scipy.optimize import newton

from ephemerista.angles import Angle

DISCRIMINATOR: Literal["anomaly_type"] = "anomaly_type"


def eccentric_to_mean(anomaly, ecc):
    return anomaly - ecc * np.sin(anomaly)


def eccentric_to_true(anomaly, ecc):
    return 2 * np.arctan(np.sqrt((1 + ecc) / (1 - ecc)) * np.tan(anomaly / 2))


def _kepler_equation(ecc_anomaly, mean_anomaly, ecc):
    return eccentric_to_mean(ecc_anomaly, ecc) - mean_anomaly


def _kepler_equation_prime(ecc_anomaly, _mean_anomaly, ecc):
    return 1 - ecc * np.cos(ecc_anomaly)


def mean_to_eccentric(anomaly, ecc):
    if -np.pi < anomaly < 0 or np.pi < anomaly:
        initial_guess = anomaly - ecc
    else:
        initial_guess = anomaly + ecc
    return newton(_kepler_equation, initial_guess, fprime=_kepler_equation_prime, args=(anomaly, ecc))


def true_to_eccentric(anomaly, ecc):
    return 2 * np.arctan(np.sqrt((1 - ecc) / (1 + ecc)) * np.tan(anomaly / 2))


class Anomaly(Angle, abc.ABC):
    degrees: float = Field(ge=-180, le=180, description="The value of the anomaly in degrees")

    @abc.abstractmethod
    def true_anomaly(self, eccentricity: float) -> float:
        """
        Returns the true anomaly of the osculating orbit in radians.

        Parameters
        ----------
        eccentricity : float
            The eccentricity of the orbit
        """
        pass

    @abc.abstractmethod
    def mean_anomaly(self, eccentricity: float) -> float:
        """
        Returns the mean anomaly of the osculating orbit in radians.

        Parameters
        ----------
        eccentricity : float
            The eccentricity of the orbit
        """
        pass


class TrueAnomaly(Anomaly):
    """Represents the true anomaly of an osculating orbit."""

    anomaly_type: Literal["true_anomaly"] = Field(
        default="true_anomaly", frozen=True, repr=False, alias="type", description="The type of the anomaly"
    )

    def true_anomaly(self, _eccentricity: float) -> float:
        return self._radians

    def mean_anomaly(self, eccentricity: float) -> float:
        return eccentric_to_mean(true_to_eccentric(self._radians, eccentricity), eccentricity)


class MeanAnomaly(Anomaly):
    """Represents the mean anomaly of an osculating orbit."""

    anomaly_type: Literal["mean_anomaly"] = Field(
        default="mean_anomaly", frozen=True, repr=False, alias="type", description="The type of the anomaly"
    )

    def true_anomaly(self, eccentricity: float) -> float:
        return eccentric_to_true(mean_to_eccentric(self._radians, eccentricity), eccentricity)

    def mean_anomaly(self, _eccentricity: float) -> float:
        return self._radians


type Anomaly = MeanAnomaly | TrueAnomaly
