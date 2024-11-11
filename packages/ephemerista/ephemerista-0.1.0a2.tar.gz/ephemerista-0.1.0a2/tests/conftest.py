import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

import ephemerista
from ephemerista.analysis.link_budget import LinkBudget
from ephemerista.analysis.visibility import Visibility
from ephemerista.assets import Asset, Spacecraft
from ephemerista.coords.trajectories import Trajectory
from ephemerista.coords.twobody import Cartesian
from ephemerista.propagators.orekit import start_orekit
from ephemerista.propagators.sgp4 import SGP4
from ephemerista.scenarios import Scenario
from ephemerista.time import Time, TimeDelta

RESOURCES = Path(__file__).parent.joinpath("resources")
EOP_PATH = RESOURCES.joinpath("finals2000A.all.csv")
ephemerista.init_provider(EOP_PATH)


@pytest.fixture(scope="session")
def iss_tle():
    return """ISS (ZARYA)
1 25544U 98067A   24187.33936543 -.00002171  00000+0 -30369-4 0  9995
2 25544  51.6384 225.3932 0010337  32.2603  75.0138 15.49573527461367"""


@pytest.fixture(scope="session")
def iss_trajectory(iss_tle):
    propagator = SGP4(tle=iss_tle)
    start_time = propagator.time
    end_time = start_time + TimeDelta.from_minutes(100)
    times = start_time.trange(end_time, step=float(TimeDelta.from_minutes(1)))
    return propagator.propagate(times)


@pytest.fixture(scope="session")
def resources():
    return RESOURCES


@pytest.fixture(scope="session")
def phasma_scenario(resources):
    json = resources.joinpath("phasma/scenario.json").read_text()
    return Scenario.model_validate_json(json)


@pytest.fixture(scope="session")
def phasma_link_budget(phasma_scenario):
    lb = LinkBudget(scenario=phasma_scenario)
    return lb.analyze()


@pytest.fixture(scope="session")
def lunar_scenario(resources):
    json = resources.joinpath("lunar/scenario.json").read_text()
    return Scenario.model_validate_json(json)


@pytest.fixture(scope="session")
def lunar_visibility(lunar_scenario):
    vis = Visibility(scenario=lunar_scenario)
    return vis.analyze()


@pytest.fixture(scope="session")
def lunar_transfer(resources):
    return Trajectory.from_csv(resources.joinpath("lunar/lunar_transfer.csv"))


@pytest.fixture(scope="session")
def root_folder(resources):
    return resources.parent.parent


@pytest.fixture(scope="session")
def start_orekit_jvm():
    return start_orekit()


@pytest.fixture(scope="session")
def maven_package(root_folder):
    java_folder = root_folder / "java_additions"
    # Try to build JAR with maven
    mvn = shutil.which("mvn")
    if mvn:
        subprocess.run([mvn, "package"], cwd=java_folder, check=True)  # noqa: S603

    return True


@pytest.fixture(scope="session")
def phasma_tle():
    return """
1 99878U 14900A   24103.76319466  .00000000  00000-0 -11394-2 0    01
2 99878  97.5138 156.7457 0016734 205.2381 161.2435 15.13998005    06"""


@pytest.fixture(scope="session")
def phasma_sc(phasma_tle):
    propagator = SGP4(tle=phasma_tle)
    return Asset(model=Spacecraft(propagator=propagator), name="PHASMA")


@pytest.fixture(scope="session")
def c0() -> Cartesian:
    """
    Returns a Cartesian state for the propagators
    """
    time = Time.from_iso("TDB", "2016-05-30T12:00:00")
    r = np.array([6068.27927, -1692.84394, -2516.61918])
    v = np.array([-0.660415582, 5.495938726, -5.303093233])

    return Cartesian.from_rv(time, r, v)
