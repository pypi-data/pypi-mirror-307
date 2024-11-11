import lox_space as lox
import pytest
from pydantic import Field

from ephemerista import BaseModel
from ephemerista.bodies import DISCRIMINATOR, Barycenter, CelestialBody, MinorBody, Planet, Satellite, Sun, _from_lox


def test_invalid():
    with pytest.raises(ValueError):
        Planet(name="Rupert")
    with pytest.raises(ValueError):
        Barycenter(name="Canopus Barycenter")
    with pytest.raises(ValueError):
        Satellite(name="Endor")
    with pytest.raises(ValueError):
        MinorBody(name="Anubis")


def test_deserialization():
    class Model(BaseModel):
        body: CelestialBody | Barycenter = Field(discriminator=DISCRIMINATOR)

    json = r'{"body": {"type": "sun"}}'
    model = Model.model_validate_json(json)
    assert isinstance(model, Model)
    assert model.body.body_type == "sun"
    assert model.body.name == "Sun"

    json = r'{"body": {"type": "barycenter", "name": "ssb"}}'
    model = Model.model_validate_json(json)
    assert isinstance(model, Model)
    assert model.body.body_type == "barycenter"
    assert model.body.name == "Solar System Barycenter"

    json = r'{"body": {"type": "planet", "name": "Earth"}}'
    model = Model.model_validate_json(json)
    assert isinstance(model, Model)
    assert model.body.body_type == "planet"
    assert model.body.name == "Earth"

    json = r'{"body": {"type": "satellite", "name": "Moon"}}'
    model = Model.model_validate_json(json)
    assert isinstance(model, Model)
    assert model.body.body_type == "satellite"
    assert model.body.name == "Moon"

    json = r'{"body": {"type": "minor_body", "name": "Ceres"}}'
    model = Model.model_validate_json(json)
    assert isinstance(model, Model)
    assert model.body.body_type == "minor_body"
    assert model.body.name == "Ceres"


def test_barycenter():
    ssb = Barycenter(name="ssb")
    assert ssb.body_type == "barycenter"
    assert ssb.name == "Solar System Barycenter"
    assert ssb.naif_id == 0
    assert ssb.gravitational_parameter == pytest.approx(132712440041.27942, rel=1e-8)


def test_sun():
    sun = Sun()
    assert sun.body_type == "sun"
    assert sun.name == "Sun"
    assert sun.naif_id == 10
    assert sun.gravitational_parameter == pytest.approx(132712440041.27942, rel=1e-8)
    assert sun.mean_radius == pytest.approx(695700.0, rel=1e-8)
    assert sun.polar_radius == pytest.approx(695700.0, rel=1e-8)
    assert sun.equatorial_radius == pytest.approx(695700.0, rel=1e-8)


def test_planet():
    earth = Planet(name="earth")
    assert earth.body_type == "planet"
    assert earth.name == "Earth"
    assert earth.naif_id == 399
    assert earth.gravitational_parameter == pytest.approx(398600.43550702266, rel=1e-8)
    assert earth.mean_radius == pytest.approx(6371.008367, rel=1e-8)
    assert earth.polar_radius == pytest.approx(6356.7519, rel=1e-8)
    assert earth.equatorial_radius == pytest.approx(6378.1366, rel=1e-8)


def test_satellite():
    moon = Satellite(name="luna")
    assert moon.body_type == "satellite"
    assert moon.name == "Moon"
    assert moon.naif_id == 301
    assert moon.mean_radius == pytest.approx(1737.4, rel=1e-8)
    assert moon.polar_radius == pytest.approx(1737.4, rel=1e-8)
    assert moon.subplanetary_radius == pytest.approx(1737.4, rel=1e-8)
    assert moon.along_orbit_radius == pytest.approx(1737.4, rel=1e-8)


def test_minor_body():
    ceres = MinorBody(name="ceres")
    assert ceres.body_type == "minor_body"
    assert ceres.name == "Ceres"
    assert ceres.naif_id == 2000001
    assert ceres.mean_radius == pytest.approx(473.5333333333333, rel=1e-8)
    assert ceres.polar_radius == pytest.approx(446.0, rel=1e-8)
    assert ceres.subplanetary_radius == pytest.approx(487.3, rel=1e-8)
    assert ceres.along_orbit_radius == pytest.approx(487.3, rel=1e-8)


def test_from_lox():
    sun = _from_lox(lox.Sun())
    assert isinstance(sun, Sun)
    ssb = _from_lox(lox.Barycenter("ssb"))
    assert isinstance(ssb, Barycenter)
    earth = _from_lox(lox.Planet("Earth"))
    assert isinstance(earth, Planet)
    moon = _from_lox(lox.Satellite("Moon"))
    assert isinstance(moon, Satellite)
    ceres = _from_lox(lox.MinorBody("Ceres"))
    assert isinstance(ceres, MinorBody)
