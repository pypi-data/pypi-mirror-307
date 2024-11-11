import pandas as pd
import pytest

from ephemerista.analysis.visibility import Visibility, Window
from ephemerista.time import Time


@pytest.fixture
def contacts(resources) -> list[Window]:
    path = resources.joinpath("lunar/contacts.csv")
    df = pd.read_csv(path, delimiter=",", converters={"start": Time.from_utc, "stop": Time.from_utc})
    windows = []
    for _, row in df.iterrows():
        start, stop = row.array
        window = Window(start=start, stop=stop)
        windows.append(window)
    return windows


def test_visibility(lunar_scenario, contacts):
    sc = lunar_scenario["Lunar Transfer"]
    gs = lunar_scenario["CEBR"]
    vis = Visibility(scenario=lunar_scenario)
    results = vis.analyze()
    windows = results[gs, sc]
    assert len(windows) == len(contacts)
    for actual, expected in zip(windows, contacts, strict=False):
        assert actual.window.start.isclose(expected.start, rtol=1e-4)
        assert actual.window.stop.isclose(expected.stop, rtol=1e-4)
