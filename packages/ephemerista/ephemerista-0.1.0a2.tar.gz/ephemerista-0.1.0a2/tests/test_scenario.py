from pathlib import Path

from ephemerista.coords.trajectories import Trajectory
from ephemerista.scenarios import Scenario

TEST_DIR = Path(__file__).parent


def test_deserialization():
    scn_json = TEST_DIR.joinpath("resources/lunar/scenario.json").resolve().read_text()
    scn = Scenario.model_validate_json(scn_json)
    assert isinstance(scn, Scenario)


def test_propagation(lunar_scenario):
    asset = lunar_scenario["Lunar Transfer"]
    ensemble = lunar_scenario.propagate()
    assert isinstance(ensemble[asset], Trajectory)
