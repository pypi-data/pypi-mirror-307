import numpy as np
import numpy.testing as npt
from pytest import approx

from ephemerista.coords.twobody import Cartesian, Keplerian
from ephemerista.time import Time


def test_elliptic():
    time = Time.from_iso("TDB", "2016-05-30T12:00:00")
    r = np.array([6068.27927, -1692.84394, -2516.61918])
    v = np.array([-0.660415582, 5.495938726, -5.303093233])

    elements = np.array(
        [
            6785.0281175534465,
            0.0006796632490758745,
            51.698121020902995,
            146.0217323119771,
            130.632025321773,
            77.57833314372851,
        ]
    )

    c = Cartesian.from_rv(time, r, v)
    k = Keplerian.from_elements(time, *elements, angle_unit="degrees")

    c1 = k.to_cartesian()
    k1 = c.to_keplerian()

    assert c1.x == approx(c.x)
    assert c1.y == approx(c.y)
    assert c1.z == approx(c.z)
    assert c1.vx == approx(c.vx)
    assert c1.vy == approx(c.vy)
    assert c1.vz == approx(c.vz)

    assert k1.semi_major_axis == approx(k.semi_major_axis)
    assert k1.eccentricity == approx(k.eccentricity)
    assert k1.inclination == approx(k.inclination)
    assert k1.ascending_node == approx(k.ascending_node)
    assert k1.periapsis_argument == approx(k.periapsis_argument)
    assert k1.true_anomaly == approx(k.true_anomaly)


def test_radii():
    elements = np.array([24464560.0, 0.7311, 0.122138, 1.00681, 3.10686, 0.44369564302687126])
    time = Time.from_iso("TDB", "2024-01-22T12:50:00")
    k = Keplerian.from_elements(time, *elements, angle_unit="radians")
    rm = k._mean_radius
    ra = k.apoapsis_radius
    rp = k.periapsis_radius
    aa = ra - rm
    ap = rp - rm
    k1 = Keplerian.from_radii(time, ra, rp, *elements[2:])
    k2 = Keplerian.from_altitudes(time, aa, ap, *elements[2:])
    assert k.semi_major_axis == approx(k1.semi_major_axis)
    assert k.semi_major_axis == approx(k2.semi_major_axis)
    assert k.eccentricity == approx(k1.eccentricity)
    assert k.eccentricity == approx(k2.eccentricity)


def test_mean_anomaly():
    elements = np.array([24464560.0, 0.7311, 0.122138, 1.00681, 3.10686, 0.44369564302687126])
    elements_mean = np.array([24464560.0, 0.7311, 0.122138, 1.00681, 3.10686, 0.04836300000000002])
    true_anomaly = elements[-1]
    mean_anomaly = elements_mean[-1]
    time = Time.from_iso("TDB", "2024-01-22T12:50:00")
    k = Keplerian.from_elements(time, *elements, angle_unit="radians")
    k1 = Keplerian.from_elements(time, *elements_mean, angle_unit="radians", anomaly_type="mean")
    assert k.true_anomaly == approx(true_anomaly)
    assert k1.true_anomaly == approx(true_anomaly)
    assert k.mean_anomaly == approx(mean_anomaly)
    assert k1.mean_anomaly == approx(mean_anomaly)


def test_lvlh():
    jd = 2.4591771079398147e6
    time = Time.from_julian_date("TDB", jd)
    semi_major = 7210.008367
    eccentricity = 0.0001807
    inclination = 51.6428
    ascending_node = 279.6468
    periapsis_arg = 68.3174
    true_anomaly = -68.2025
    k = Keplerian.from_elements(
        time, semi_major, eccentricity, inclination, ascending_node, periapsis_arg, true_anomaly
    )
    s = k.to_cartesian()
    rot = s.rotation_lvlh()
    r = s.position
    rn = r / np.linalg.norm(r)
    v = s.velocity
    vn = v / np.linalg.norm(v)
    npt.assert_allclose(rot.T @ vn, np.array([1, 0, 0]), atol=1e-3)
    npt.assert_allclose(rot.T @ -rn, np.array([0, 0, 1]), atol=1e-3)
