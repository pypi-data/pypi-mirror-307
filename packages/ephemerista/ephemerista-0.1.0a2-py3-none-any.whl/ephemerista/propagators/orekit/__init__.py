import abc
import os
import platform
from pathlib import Path

import numpy as np
import orekit_jpype
from pydantic import Field, PrivateAttr

from ephemerista.bodies import CelestialBody
from ephemerista.coords.trajectories import Trajectory
from ephemerista.coords.twobody import Cartesian, TwoBody
from ephemerista.propagators import Propagator
from ephemerista.propagators.events import StoppingEvent
from ephemerista.propagators.orekit.conversions import (
    cartesian_to_tpv,
    time_to_abs_date,
    time_to_j2000_tai,
    tpv_to_cartesian,
)
from ephemerista.time import Time

JVM = {
    "Darwin": os.path.join("lib", "server", "libjvm.dylib"),
    "Linux": os.path.join("lib", "server", "libjvm.so"),
    "Windows": os.path.join("bin", "server", "jvm.dll"),
}[platform.system()]


def start_orekit(
    jvmpath: str | os.PathLike | None = None,
    filenames: str | list[str] | None = None,
    from_pip_library: bool = True,  # noqa: FBT001, FBT002
) -> None:
    """
    Start the JVM for Orekit jpype, and loads the orekitdata library.

    Parameters
    ----------
    jvmpath: str | os.PathLike | None
        Path to the JVM. If None, it will be loaded from jdk4py or from the JAVA_HOME environment variable
        See https://gitlab.orekit.org/orekit/orekit_jpype/-/blob/a152ff535e16edcaba633521ebeba7865e870587/orekit_jpype/orekit_jpype.py#L12
    filenames: str | list[str]
        Name of zip or folder with orekit data. Default filename is 'orekit-data.zip'
        See https://gitlab.orekit.org/orekit/orekit_jpype/-/blob/a152ff535e16edcaba633521ebeba7865e870587/orekit_jpype/pyhelpers.py#L155
    from_pip_library: bool
        If True, will first try to load the data from the `orekitdata` python library
        See https://gitlab.orekit.org/orekit/orekit_jpype/-/blob/a152ff535e16edcaba633521ebeba7865e870587/orekit_jpype/pyhelpers.py#L155
    """
    ephemerista_jar = Path(__file__).parent.parent.parent / "jars" / "ephemeristaJava-0.0.1-SNAPSHOT.jar"
    if not ephemerista_jar.is_file():
        msg = f"{ephemerista_jar} not found"
        raise FileNotFoundError(msg)
    additional_classpaths = [str(ephemerista_jar)]

    if (jvmpath is None) and ("JAVA_HOME" not in os.environ):
        import jdk4py

        jvmpath = os.path.join(jdk4py.JAVA_HOME, JVM)

    orekit_jpype.initVM(additional_classpaths=additional_classpaths, jvmpath=jvmpath)

    return orekit_jpype.pyhelpers.setup_orekit_data(filenames=filenames, from_pip_library=from_pip_library)


class OrekitPropagator(Propagator, abc.ABC):
    state_init: TwoBody

    prop_min_step: float = Field(default=0.001)  # s
    prop_max_step: float = Field(default=3600.0)  # s
    prop_init_step: float = Field(default=60.0)  # s
    prop_position_error: float = Field(default=10.0)  # m

    mass: float = Field(default=1000.0)  # kg
    cross_section: float = Field(default=1.0)  # m^2

    grav_degree_order: tuple[int, int] | None = Field(default=(4, 4))

    third_bodies: list[CelestialBody] = Field(default=[])

    c_r: float = Field(default=0.75)
    enable_srp: bool = Field(default=False)

    c_d: float = Field(default=2.0)
    enable_drag: bool = Field(default=False)

    _orekit_prop = PrivateAttr()
    _wgs84_ellipsoid = PrivateAttr()
    _sun = PrivateAttr()
    _icrf = PrivateAttr()

    def __init__(
        self,
        jvmpath: str | os.PathLike | None = None,
        filenames: str | list[str] | None = None,
        from_pip_library: bool = True,  # noqa: FBT001, FBT002
        gravity_file: Path | None = None,
        **data,
    ):
        """
        If a gravity potential coefficients files is supplied, the default Orekit ones (Earth EIGEN-6S) will be
        discarded before adding the provided coefficient file, so use with care
        """
        super().__init__(**data)
        start_orekit(
            jvmpath=jvmpath,
            filenames=filenames,
            from_pip_library=from_pip_library,
        )

        self.add_gravity_file(gravity_file)

        self.setup_orekit_objs()

    def add_gravity_file(self, gravity_file: Path | None = None):
        if gravity_file is None:
            return

        from java.io import File  # type: ignore
        from org.orekit.data import DataContext, DirectoryCrawler  # type: ignore
        from org.orekit.errors import OrekitException  # type: ignore
        from org.orekit.forces.gravity.potential import (  # type: ignore
            EGMFormatReader,
            GravityFieldFactory,
            GRGSFormatReader,
            ICGEMFormatReader,
            SHMFormatReader,
        )

        gravity_readers = [EGMFormatReader, GRGSFormatReader, ICGEMFormatReader, SHMFormatReader]

        dm = DataContext.getDefault().getDataProvidersManager()
        GravityFieldFactory.clearPotentialCoefficientsReaders()

        folder = gravity_file.parent
        dm.addProvider(DirectoryCrawler(File(str(folder.absolute()))))  # add folder to Orekit data providers manager

        for gravity_reader in gravity_readers:
            try:
                coeff_reader = gravity_reader(gravity_file.name, True)
                GravityFieldFactory.addPotentialCoefficientsReader(coeff_reader)
                GravityFieldFactory.readGravityField(4, 4)  # Test reading until degree/order 4
                break
            except OrekitException:
                # This format reader was the wrong one, we clear the list of readers and will try the next one
                GravityFieldFactory.clearPotentialCoefficientsReaders()
                continue

    def setup_orekit_objs(self):
        from org.orekit.frames import FramesFactory  # type: ignore

        self._icrf = FramesFactory.getGCRF()  # Earth-centered ICRF
        from org.orekit.utils import IERSConventions  # type: ignore

        itrf = FramesFactory.getITRF(IERSConventions.IERS_2010, False)
        from org.orekit.models.earth import ReferenceEllipsoid  # type: ignore

        self._wgs84_ellipsoid = ReferenceEllipsoid.getWgs84(itrf)

        from org.orekit.bodies import CelestialBodyFactory  # type: ignore

        self._sun = CelestialBodyFactory.getSun()

        from org.orekit.orbits import CartesianOrbit, EquinoctialOrbit  # type: ignore
        from org.orekit.utils import Constants as OrekitConstants  # type: ignore

        tpv_icrf = cartesian_to_tpv(self.state_init.to_cartesian())
        orbit_init_cart = CartesianOrbit(tpv_icrf, self._icrf, OrekitConstants.EIGEN5C_EARTH_MU)
        orbit_init_equinoctial = EquinoctialOrbit(orbit_init_cart)
        self.setup_propagator(orbit_init_equinoctial)
        self.set_initial_state(self.state_init)

    @abc.abstractmethod
    def setup_propagator(self, orbit_sample): ...

    def set_initial_state(self, state_init: TwoBody):
        from org.orekit.orbits import CartesianOrbit, EquinoctialOrbit  # type: ignore
        from org.orekit.utils import Constants as OrekitConstants  # type: ignore

        tpv_icrf = cartesian_to_tpv(state_init.to_cartesian())
        orbit_init_cart = CartesianOrbit(tpv_icrf, self._icrf, OrekitConstants.EIGEN5C_EARTH_MU)
        orbit_init_equinoctial = EquinoctialOrbit(orbit_init_cart)
        from org.orekit.propagation import SpacecraftState  # type: ignore

        state_init_orekit = SpacecraftState(orbit_init_equinoctial, self.mass)
        self._orekit_prop.resetInitialState(state_init_orekit)

    def add_stop_condition(self, stop_cond: StoppingEvent):
        if stop_cond == StoppingEvent.PERIAPSIS:
            from org.orekit.propagation.events import ApsideDetector  # type: ignore
            from org.orekit.propagation.events.handlers import StopOnIncreasing  # type: ignore

            periapsis_detector = ApsideDetector(self._orekit_prop.getInitialState().getOrbit()).withHandler(
                StopOnIncreasing()
            )
            self._orekit_prop.addEventDetector(periapsis_detector)
        elif stop_cond == StoppingEvent.APOAPSIS:
            from org.orekit.propagation.events import ApsideDetector  # type: ignore
            from org.orekit.propagation.events.handlers import StopOnDecreasing  # type: ignore

            apoapsis_detector = ApsideDetector(self._orekit_prop.getInitialState().getOrbit()).withHandler(
                StopOnDecreasing()
            )
            self._orekit_prop.addEventDetector(apoapsis_detector)

    def propagate(
        self,
        time: Time | list[Time],
        stop_conds: list[StoppingEvent] | None = None,
    ) -> Cartesian | Trajectory:
        """
        When stopping conditions are defined, the Trajectory will end at the stopping condition so
        it won't contain all the states requested in the input Time list.
        """
        self.set_initial_state(self.state_init)

        if stop_conds:
            self._orekit_prop.clearEventsDetectors()
            for stop_cond in stop_conds:
                self.add_stop_condition(stop_cond)

        if isinstance(time, Time):
            state_end = self._orekit_prop.propagate(time_to_abs_date(time))
            return tpv_to_cartesian(state_end.getPVCoordinates())
        else:
            eph_generator = self._orekit_prop.getEphemerisGenerator()
            time_start = time[0]
            time_end = time[-1]
            self._orekit_prop.propagate(time_to_abs_date(time_end))
            bounded_propagator = eph_generator.getGeneratedEphemeris()

            from org.lsf.OrekitConversions import exportStates2D

            # Exporting states to 2D array in Java, and writing the memory content to a numpy array
            time_j2000_list = [time_to_j2000_tai(t) for t in time]  # TODO: prevent using a for loop
            states_array = np.asarray(memoryview(exportStates2D(bounded_propagator, time_j2000_list)))

            return Trajectory(start_time=time_start, states=states_array)
