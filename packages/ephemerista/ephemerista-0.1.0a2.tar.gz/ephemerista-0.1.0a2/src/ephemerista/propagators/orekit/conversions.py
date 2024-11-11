from math import floor

import numpy as np

from ephemerista.coords.anomalies import MeanAnomaly
from ephemerista.coords.twobody import Cartesian, Keplerian
from ephemerista.time import SecondsTimestamp, Time


def time_to_j2000_tai(time: Time) -> float:
    time_tai = time.to_scale("TAI")
    return time_tai._time.seconds() + time_tai._time.subsecond()


def time_to_abs_date(time: Time):
    """
    Converts a Time to an Orekit AbsoluteDate, after having converted the Time object to TAI scale
    """
    from org.orekit.time import AbsoluteDate, TimeScalesFactory  # type: ignore

    j2000_epoch_tai = AbsoluteDate(2000, 1, 1, 12, 0, 0.0, TimeScalesFactory.getTAI())
    return AbsoluteDate(j2000_epoch_tai, time_to_j2000_tai(time), TimeScalesFactory.getTAI())


def abs_date_to_time(abs_date) -> Time:
    """
    Returns the Time representation of the given AbsoluteDate, in TAI scale
    """
    from org.orekit.time import AbsoluteDate, TimeScalesFactory  # type: ignore

    j2000_epoch_tai = AbsoluteDate(2000, 1, 1, 12, 0, 0.0, TimeScalesFactory.getTAI())
    j2000_float = abs_date.durationFrom(j2000_epoch_tai)
    j2000_seconds = int(floor(j2000_float))
    j2000_subsecond = j2000_float - j2000_seconds
    return Time(scale="TAI", timestamp=SecondsTimestamp(seconds=j2000_seconds, subsecond=j2000_subsecond))


def cartesian_to_tpv(cart: Cartesian):
    from org.hipparchus.geometry.euclidean.threed import Vector3D  # type: ignore

    pos_icrf = Vector3D(cart.x * 1e3, cart.y * 1e3, cart.z * 1e3)
    vel_icrf = Vector3D(cart.vx * 1e3, cart.vy * 1e3, cart.vz * 1e3)
    from org.orekit.utils import TimeStampedPVCoordinates  # type: ignore

    return TimeStampedPVCoordinates(time_to_abs_date(cart.time), pos_icrf, vel_icrf)


def tpv_to_cartesian(tpv) -> Cartesian:
    return Cartesian.from_rv(
        time=abs_date_to_time(tpv.getDate()),
        r=1e-3 * np.array(tpv.getPosition().toArray()),
        v=1e-3 * np.array(tpv.getVelocity().toArray()),
    )


def orekit_to_keplerian(kepl_orekit) -> Keplerian:
    return Keplerian.from_elements(
        time=abs_date_to_time(kepl_orekit.getDate()),
        semi_major_axis=kepl_orekit.getA() * 1e-3,
        eccentricity=kepl_orekit.getE(),
        inclination=np.rad2deg(kepl_orekit.getI()),
        ascending_node=np.rad2deg(kepl_orekit.getRightAscensionOfAscendingNode()),
        periapsis_argument=np.rad2deg(kepl_orekit.getPerigeeArgument()),
        anomaly=np.rad2deg(kepl_orekit.getMeanAnomaly()),
        anomaly_type=MeanAnomaly,
    )
