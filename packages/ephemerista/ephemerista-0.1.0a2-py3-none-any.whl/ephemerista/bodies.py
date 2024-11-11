import abc
from typing import Literal, Self

import lox_space as lox
import numpy as np
import plotly.graph_objects as go
from pydantic import Field, PrivateAttr

from ephemerista import BaseModel

DISCRIMINATOR: Literal["body_type"] = "body_type"


class Barycenter(BaseModel):
    """
    Barycenter of the Solar System or one of the satellite systems of the Solar System with associated physical
    constants
    """

    body_type: Literal["barycenter"] = Field(
        default="barycenter",
        frozen=True,
        repr=False,
        alias="type",
        description="The type of the celestial body",
    )
    name: str = Field(description="The name of the barycenter")
    _body: lox.Barycenter = PrivateAttr()

    def __init__(self, body: lox.Barycenter | None = None, **data):
        super().__init__(**data)
        if not body:
            self._body = lox.Barycenter(self.name)
            self.name = self._body.name()
        else:
            self._body = body

    @classmethod
    def _from_lox(cls, body: lox.Barycenter) -> Self:
        name = body.name()
        return cls(body=body, name=name)

    @property
    def naif_id(self) -> int:
        """int: The NAIF ID of the barycenter"""
        return self._body.id()

    @property
    def gravitational_parameter(self) -> float:
        """float: The gravitational parameter of the barycenter [km^3/s^2]"""
        return self._body.gravitational_parameter()


class Body(BaseModel, abc.ABC):
    @property
    @abc.abstractmethod
    def naif_id(self) -> int:
        """int: The NAIF ID of the celestial body"""
        pass

    @property
    @abc.abstractmethod
    def gravitational_parameter(self) -> float:
        """float: The gravitational parameter of the celestial body [km^3/s^2]"""
        pass

    @property
    @abc.abstractmethod
    def mean_radius(self) -> float:
        """float: The mean radius of the celestial body [km]"""
        pass

    @property
    @abc.abstractmethod
    def polar_radius(self) -> float:
        """float: The polar radius of the celestial body [km]"""
        pass

    def plot_3d_surface(self) -> go.Mesh3d:
        phi = np.linspace(0, 2 * np.pi)
        theta = np.linspace(-np.pi / 2, np.pi / 2)
        phi, theta = np.meshgrid(phi, theta)
        x = np.cos(theta) * np.sin(phi) * self.mean_radius
        y = np.cos(theta) * np.cos(phi) * self.mean_radius
        z = np.sin(theta) * self.mean_radius
        x, y, z = np.vstack([x.ravel(), y.ravel(), z.ravel()])
        return go.Mesh3d(x=x, y=y, z=z, alphahull=0, name=self._body.name())


class Sun(Body):
    """The Sun with associated physical constants"""

    body_type: Literal["sun"] = Field(
        default="sun",
        frozen=True,
        repr=False,
        alias="type",
        description="The type of the celestial body",
    )
    _body: lox.Sun = PrivateAttr()
    _name: str = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._body = lox.Sun()
        self._name = self._body.name()

    @property
    def naif_id(self) -> int:
        return self._body.id()

    @property
    def name(self) -> str:
        return self._name

    @property
    def gravitational_parameter(self) -> float:
        return self._body.gravitational_parameter()

    @property
    def mean_radius(self) -> float:
        return self._body.mean_radius()

    @property
    def polar_radius(self) -> float:
        return self._body.polar_radius()

    @property
    def equatorial_radius(self) -> float:
        """float: The equatorial radius of the celestial body [km]"""
        return self._body.equatorial_radius()


class Planet(Body):
    """Planet of the Solar System with associated physical constants"""

    body_type: Literal["planet"] = Field(
        default="planet",
        frozen=True,
        repr=False,
        alias="type",
        description="The type of the celestial body",
    )
    name: str = Field(description="The name of the planet")
    _body: lox.Planet = PrivateAttr()

    def __init__(self, body: lox.Planet | None = None, **data):
        super().__init__(**data)
        if not body:
            self._body = lox.Planet(self.name)
            self.name = self._body.name()
        else:
            self._body = body

    @classmethod
    def _from_lox(cls, body: lox.Planet) -> Self:
        name = body.name()
        return cls(body=body, name=name)

    @property
    def naif_id(self) -> int:
        return self._body.id()

    @property
    def gravitational_parameter(self) -> float:
        return self._body.gravitational_parameter()

    @property
    def mean_radius(self) -> float:
        return self._body.mean_radius()

    @property
    def polar_radius(self) -> float:
        return self._body.polar_radius()

    @property
    def equatorial_radius(self) -> float:
        """float: The equatorial radius of the celestial body [km]"""
        return self._body.equatorial_radius()


class Satellite(Body):
    """Natural satellite of the Solar System with associated physical constants"""

    body_type: Literal["satellite"] = Field(
        default="satellite",
        frozen=True,
        repr=False,
        alias="type",
        description="The type of the celestial body",
    )
    name: str = Field(description="The name of the natural satellite")
    _body: lox.Satellite = PrivateAttr()

    def __init__(self, body: lox.Satellite | None = None, **data):
        super().__init__(**data)
        if not body:
            self._body = lox.Satellite(self.name)
            self.name = self._body.name()
        else:
            self._body = body

    @classmethod
    def _from_lox(cls, body: lox.Satellite) -> Self:
        name = body.name()
        return cls(body=body, name=name)

    @property
    def naif_id(self) -> int:
        return self._body.id()

    @property
    def gravitational_parameter(self) -> float:
        return self._body.gravitational_parameter()

    @property
    def mean_radius(self) -> float:
        return self._body.mean_radius()

    @property
    def polar_radius(self) -> float:
        return self._body.polar_radius()

    @property
    def subplanetary_radius(self) -> float:
        """float: The subplanetary radius of the celestial body [km]"""
        return self._body.subplanetary_radius()

    @property
    def along_orbit_radius(self) -> float:
        """float: The along-orbit radius of the celestial body [km]"""
        return self._body.along_orbit_radius()


class MinorBody(Body):
    """Minor body of the Solar System with associated physical constants"""

    body_type: Literal["minor_body"] = Field(
        default="minor_body",
        frozen=True,
        repr=False,
        alias="type",
        description="The type of the celestial body",
    )
    name: str = Field(description="The name of the minor body")
    _body: lox.MinorBody = PrivateAttr()

    def __init__(self, body: lox.MinorBody | None = None, **data):
        super().__init__(**data)
        if not body:
            self._body = lox.MinorBody(self.name)
            self.name = self._body.name()
        else:
            self._body = body

    @classmethod
    def _from_lox(cls, body: lox.MinorBody) -> Self:
        name = body.name()
        return cls(body=body, name=name)

    @property
    def naif_id(self) -> int:
        return self._body.id()

    @property
    def gravitational_parameter(self) -> float:
        return self._body.gravitational_parameter()

    @property
    def mean_radius(self) -> float:
        return self._body.mean_radius()

    @property
    def polar_radius(self) -> float:
        return self._body.polar_radius()

    @property
    def subplanetary_radius(self) -> float:
        """float: The subplanetary radius of the celestial body [km]"""
        return self._body.subplanetary_radius()

    @property
    def along_orbit_radius(self) -> float:
        """float: The along-orbit radius of the celestial body [km]"""
        return self._body.along_orbit_radius()


type CelestialBody = Sun | Planet | Satellite | MinorBody


def _from_lox(
    body: lox.Sun | lox.Barycenter | lox.Planet | lox.Satellite | lox.MinorBody,
) -> CelestialBody | Barycenter:
    if isinstance(body, lox.Sun):
        return Sun()
    elif isinstance(body, lox.Barycenter):
        return Barycenter._from_lox(body)
    elif isinstance(body, lox.Planet):
        return Planet._from_lox(body)
    elif isinstance(body, lox.Satellite):
        return Satellite._from_lox(body)
    elif isinstance(body, lox.MinorBody):
        return MinorBody._from_lox(body)
    pass
