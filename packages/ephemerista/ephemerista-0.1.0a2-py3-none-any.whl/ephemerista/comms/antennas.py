import abc
import math
from typing import Literal

import numpy as np
import plotly.graph_objects as go
import pydantic_numpy.typing as pnd
import scipy
from numpy.typing import ArrayLike
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from ephemerista import BaseModel, Vec3
from ephemerista.angles import Angle
from ephemerista.comms.utils import to_db, wavelength

ANTENNA_DISCRIMINATOR = "antenna_type"
PATTERN_DISCRIMINATOR = "pattern_type"

"""
When dividing by a quantity, if this quantity is lower than this threshold,
an alternate formulation will be used to avoid division by zero
"""
DIV_BY_ZERO_LIMIT = 1e-6

"""
Represents the lowest gain value in linear representation, because zero gain
would lead to an error when converting to dB.
This value represents a signal strength in dB so low that no link will probably be possible.
"""
MINF_GAIN_LINEAR = 1e-12

SHORT_DIPOLE_LIMIT = 0.1  # when length/wavelength lower than this value, it is officially a short dipole


class FieldOfRegard(Angle):
    degrees: float = Field(
        ge=0.0,
        le=90.0,
        default=0.0,
        description="Field of regard half-cone angle in degrees",
    )


class Antenna(BaseModel, abc.ABC):
    design_frequency: float | None = Field(
        gt=0.0, default=None, description="The design frequency of the antenna in Hz"
    )
    field_of_regard: FieldOfRegard = Field(
        description=(
            "Defines a cone around the boresight vector in which a movable antenna can operate."
            "The value is the half-angle of the cone in degrees. A value of 0.0 indicates a fixed antenna."
        ),
        default=FieldOfRegard(),
    )
    boresight_vector: Vec3 = Field(
        description="The boresight vector of the antenna in the local reference frame",
        default=(0.0, 0.0, 1.0),
    )

    @abc.abstractmethod
    def gain(self, frequency: float, angle: float) -> float:
        raise NotImplementedError()

    @abc.abstractmethod
    def beamwidth(self, frequency: float) -> float:
        raise NotImplementedError()

    @property
    def boresight_array(self) -> np.ndarray:
        return np.array(self.boresight_vector)


class SimpleAntenna(Antenna):
    antenna_type: Literal["simple"] = Field(default="simple", alias="type", repr=False, frozen=True)
    gain_db: float = Field(ge=0.0, json_schema_extra={"title": "Gain"})
    beamwidth_deg: float = Field(ge=0.0, json_schema_extra={"title": "Beamwidth"})

    def gain(self, _frequency: float, _angle: float) -> float:
        return self.gain_db

    def beamwidth(self, _frequency: float) -> float:
        return self.beamwidth_deg


class Pattern(BaseModel, abc.ABC):
    @abc.abstractmethod
    def gain(self, frequency: float, angle: float) -> float:
        raise NotImplementedError()

    @abc.abstractmethod
    def beamwidth(self, frequency: float) -> float:
        raise NotImplementedError()


class ParabolicPattern(Pattern):
    pattern_type: Literal["parabolic"] = Field(default="parabolic")
    diameter: float = Field(gt=0.0)
    efficiency: float = Field(gt=0.0)

    bessel_first_root: float = scipy.special.jn_zeros(1, 1)[0]

    def area(self) -> float:
        return math.pi * self.diameter**2 / 4

    def beamwidth(self, frequency: float) -> float:
        """
        Computes the half-cone angle of the half-power beamwidth in radians
        Source: https://en.wikipedia.org/wiki/Parabolic_antenna
        """
        return np.arcsin(self.bessel_first_root * wavelength(frequency) / np.pi / self.diameter)

    def peak_gain(self, frequency: float) -> float:
        area = self.area()
        lamb = wavelength(frequency)
        g = to_db(4 * math.pi * area / lamb**2)
        return g + to_db(self.efficiency)

    def gain(self, frequency: float, angle: ArrayLike) -> pnd.Np1DArrayFp64:
        """
        Computes the gain of a parabolic antenna for a direction given by the angle `_angle`
        Assumes an uniform illuminated aperture (i.e. taper parameter $\tau$ = 1.0)
        Source: Equation (17) of https://web.archive.org/web/20160101021857/https://library.nrao.edu/public/memos/alma/memo456.pdf
        """
        u = np.pi * self.diameter / wavelength(frequency) * np.sin(angle)

        with np.testing.suppress_warnings() as sup:
            # Ugly but otherwise we get 'RuntimeWarning: invalid value encountered in scalar divide' warnings,
            # but we actually don't use the values issuing these warnings thanks to the np.where call
            sup.filter(RuntimeWarning)

            pattern_loss_linear = np.where(
                np.abs(u) < DIV_BY_ZERO_LIMIT,  # Preventing division by zero at zero angle
                1.0,  # Maximum gain (relative to peak gain)
                np.square(2 * scipy.special.jv(1, u) / u),
            )
            # Setting very low gain at angles higher than 45 degrees
            # This is because the pattern equation used is symmetrical, that would result in
            # the backlobe having the same gain as the main lobe, which is wrong...

            # Besides, this equation also does not model spillover radation from the feed missing the reflector,
            # so it does not make sense to use it for high angles.
            # For basically any parabolic antenna, if the depointing is higher than 45 degrees,
            # you will barely receive anything...
            pattern_loss_linear = np.where(
                np.cos(angle) < np.cos(np.pi / 4),
                MINF_GAIN_LINEAR,  # very small value otherwise conversion to dB fails
                pattern_loss_linear,
            )

            return self.peak_gain(frequency=frequency) + to_db(pattern_loss_linear)


class CustomPattern(Pattern):
    pattern_type: Literal["custom"] = Field(default="custom")
    # Skipping because it cannot be displayed by the form widget
    angles: SkipJsonSchema[pnd.Np1DArrayFp64]
    # Skipping because it cannot be displayed by the form widget
    gains: SkipJsonSchema[pnd.Np1DArrayFp64]
    symmetrical: bool = Field(default=True)

    def beamwidth(self, _frequency: float) -> float:
        """
        Returns 180 degrees, because the concept of beamwidth is undefined with a custom pattern...
        """
        return np.pi

    def gain(self, _frequency: float, angle: ArrayLike) -> pnd.Np1DArrayFp64:
        # TODO: Handle symmetry and out-of-range angles
        return np.interp(angle, self.angles, self.gains)  # type: ignore

    def peak_gain(self, _frequency: float) -> float:
        return np.max(self.gains)


class DipolePattern(Pattern):
    pattern_type: Literal["dipole"] = Field(default="dipole")
    length: float = Field(gt=0.0)

    def beamwidth(self, _frequency: float) -> float:
        """
        Returns 180 degrees, because the concept of beamwidth is undefined with dipole antennas:
          a dipole antennas has several main lobes of sometimes different widths
        """
        return np.pi

    def gain_pattern(self, frequency: float, angle: ArrayLike) -> pnd.Np1DArrayFp64:
        """
        Returns the gain relative to the peak gain, in linear units, between 0 and 1
        Source 1: Slide 17 of https://www.brown.edu/research/labs/mittleman/sites/brown.edu.research.labs.mittleman/files/uploads/lecture25.pdf
        Source 2: https://www.antenna-theory.com/antennas/dipole.php
        Source 3: https://en.wikipedia.org/wiki/Dipole_antenna#Short_dipole
        Source 4: https://www.antenna-theory.com/antennas/shortdipole.php
        """
        with np.testing.suppress_warnings() as sup:
            # TODO: Ugly but otherwise we get 'RuntimeWarning: divide by zero encountered in scalar divide' warnings,
            # but we actually don't use the values issuing these warnings thanks to the np.where call
            sup.filter(RuntimeWarning)

            k = 2 * np.pi / wavelength(frequency=frequency)
            kl2 = k * self.length / 2

            return np.where(
                np.abs(np.sin(angle)) < DIV_BY_ZERO_LIMIT,  # Avoid division by zero when np.sin(angle) is small
                MINF_GAIN_LINEAR,  # very small value otherwise the conversion to dB is not happy
                np.where(
                    self.length / wavelength(frequency=frequency) < SHORT_DIPOLE_LIMIT,
                    np.square(np.sin(angle)),  # Alternative formulation for short dipole
                    np.square((np.cos(kl2 * np.cos(angle)) - np.cos(kl2)) / np.sin(angle)),  # General dipole
                ),
            )

    def directivity(self, frequency: float) -> float:
        integral, err = scipy.integrate.quad(
            lambda angle, frequency: self.gain_pattern(frequency=frequency, angle=angle) * np.sin(angle),
            0,
            np.pi,
            args=(frequency,),
        )
        return 2 / integral

    def peak_gain(self, frequency: float) -> float:
        optimum = scipy.optimize.minimize_scalar(lambda x: -to_db(self.gain_pattern(frequency=frequency, angle=x)))
        return -optimum.fun + to_db(self.directivity(frequency=frequency))

    def gain(self, frequency: float, angle: ArrayLike) -> pnd.Np1DArrayFp64:
        return to_db(self.directivity(frequency=frequency)) + to_db(self.gain_pattern(frequency=frequency, angle=angle))


type PatternType = ParabolicPattern | CustomPattern | DipolePattern


class ComplexAntenna(Antenna):
    antenna_type: Literal["complex"] = Field(default="complex", alias="type", repr=False, frozen=True)
    pattern: PatternType = Field(discriminator=PATTERN_DISCRIMINATOR)

    def gain(self, frequency: float, angle: ArrayLike) -> pnd.Np1DArrayFp64:
        return self.pattern.gain(frequency, angle)

    def beamwidth(self, frequency: float) -> float:
        return self.pattern.beamwidth(frequency)

    def peak_gain(self, frequency: float) -> float:
        return self.pattern.peak_gain(frequency=frequency)

    def plot_pattern(
        self,
        frequency: float,
        fig_style: str = "polar",
        trace_name: str | None = None,
        *,
        relative_to_peak: bool = False,
    ) -> go.Scatterpolar | go.Scatter:
        theta_array = np.arange(-np.pi, np.pi, 1e-3)
        gain_array = self.gain(frequency=frequency, angle=theta_array)
        if relative_to_peak:
            gain_array = gain_array - self.peak_gain(frequency=frequency)

        if fig_style == "polar":
            return go.Scatterpolar(
                r=gain_array,
                theta=np.rad2deg(theta_array),
                mode="lines",
                name=trace_name,
            )

        elif fig_style == "linear":
            return go.Scatter(y=gain_array, x=np.rad2deg(theta_array), mode="lines", name=trace_name)


type AntennaType = SimpleAntenna | ComplexAntenna
