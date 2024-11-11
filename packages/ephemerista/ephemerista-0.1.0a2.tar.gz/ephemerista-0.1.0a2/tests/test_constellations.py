import json
from pathlib import Path

import pytest

from ephemerista.constellation.design import AbstractConstellation, WalkerDelta, WalkerStar
from ephemerista.coords.twobody import Keplerian
from ephemerista.propagators.orekit.numerical import NumericalPropagator
from ephemerista.propagators.orekit.semianalytical import SemiAnalyticalPropagator
from ephemerista.scenarios import Scenario
from ephemerista.time import Time, TimeDelta


def test_walker_star_not_physical():
    time = Time.from_iso("TDB", "2016-05-30T12:00:00")

    # Case 2. Invalid constellation, not physical
    with pytest.raises(ValueError, match="The constellation is not physical: Perigee crosses Earth's Radius!"):
        WalkerStar(
            time=time,
            nsats=10,
            nplanes=2,
            semi_major_axis=3000,
            inclination=45,
            eccentricity=0.0,
            periapsis_argument=90,
        )


def test_walker_star_wrong_nplanes_nsats_multiple():
    time = Time.from_iso("TDB", "2016-05-30T12:00:00")

    # Case 3. Invalid constellation, wrong number of planes
    with pytest.raises(
        ValueError,
        match="The number of satellites per plane must be a multiple of the number of planes for a constellation.",
    ):
        WalkerStar(
            time=time,
            nsats=47,
            nplanes=6,
            semi_major_axis=7000,
            inclination=45,
            eccentricity=0.0,
            periapsis_argument=90,
        )


def test_walker_star_wrong_phasing():
    time = Time.from_iso("TDB", "2016-05-30T12:00:00")

    # Case 2. Invalid constellation, not physical
    with pytest.raises(
        ValueError,
        match="The number of satellites per plane must be a multiple of the number of planes for a constellation.",
    ):
        WalkerStar(
            time=time,
            nsats=64,
            nplanes=6,
            semi_major_axis=7000,
            inclination=45,
            eccentricity=0.0,
            periapsis_argument=90,
            phasing=10,
        )


OREKIT_PROP_CLASSES = [NumericalPropagator, SemiAnalyticalPropagator]


@pytest.mark.parametrize("orekit_prop", OREKIT_PROP_CLASSES)
def test_scenario_minimal(orekit_prop, c0):
    prop_templ = orekit_prop(state_init=c0)  # the state c0 will not actually be used
    start_time = Time.from_iso("TDB", "2016-05-30T12:00:00")
    duration_hours = 2.0

    nsats = 16
    ws = WalkerStar(
        time=start_time,
        nsats=nsats,
        nplanes=8,
        semi_major_axis=7000,
        inclination=45,
        eccentricity=0.0,
        periapsis_argument=90,
    )

    scenario_templ = Scenario(
        name="Constellation",
        start_time=start_time,
        end_time=start_time + TimeDelta.from_hours(duration_hours),
    )

    assert len(scenario_templ.assets) == 0

    scenario_with_sats = ws.gen_scenario(scenario_templ, prop_templ)

    assert len(scenario_with_sats.assets) == nsats

    name_list_actual = [asset.name for asset in scenario_with_sats.assets]
    name_list_expected = []
    for state_init in ws.satellites:
        name_list_expected.append(state_init.satellite_name)

    for name_actual, name_expected in zip(sorted(name_list_actual), sorted(name_list_expected), strict=False):
        assert name_actual == name_expected


def compare_against_matlab_json(json_path: Path, constellation: AbstractConstellation):
    with open(json_path) as f:
        ws_matlab_json_raw = json.load(f)
        ws_matlab_satellites = ws_matlab_json_raw["satellites"]

    for i, matlab_sat_dict in enumerate(ws_matlab_satellites):
        matlab_sat = Keplerian.model_validate(matlab_sat_dict)
        # Overwriting satellite name because Matlab uses different naming conventions for constellation satellites
        matlab_sat.satellite_name = constellation.satellites[i].satellite_name
        assert matlab_sat == constellation.satellites[i]


def test_against_matlab_ws_1(resources):
    start_time = Time.from_iso("TDB", "2016-05-30T12:00:00")
    ws_ephemerista = WalkerStar(
        time=start_time,
        nsats=64,
        nplanes=8,
        semi_major_axis=7000,
        inclination=45,
        eccentricity=0.0,
        periapsis_argument=0,
        phasing=2,
        name="constellation1",
    )

    compare_against_matlab_json(resources / "constellation" / "constellation1_walker_star_matlab.json", ws_ephemerista)


def test_against_matlab_ws_oneweb(resources):
    start_time = Time.from_iso("TDB", "2016-05-30T12:00:00")
    ws_ephemerista = WalkerStar(
        time=start_time,
        nsats=648,
        nplanes=18,
        semi_major_axis=7578,
        inclination=86.4,
        eccentricity=0.0,
        periapsis_argument=0,
        name="oneweb",
    )

    compare_against_matlab_json(resources / "constellation" / "oneweb_walker_star_matlab.json", ws_ephemerista)


def test_against_matlab_wd_1(resources):
    start_time = Time.from_iso("TDB", "2016-05-30T12:00:00")
    wd_ephemerista = WalkerDelta(
        time=start_time,
        nsats=72,
        nplanes=9,
        semi_major_axis=7000,
        inclination=98.0,
        eccentricity=0.0,
        periapsis_argument=0,
        phasing=4,
        name="constellation2",
    )

    compare_against_matlab_json(resources / "constellation" / "constellation2_walker_delta_matlab.json", wd_ephemerista)


def test_against_matlab_wd_galileo_like(resources):
    start_time = Time.from_iso("TDB", "2016-05-30T12:00:00")
    wd_ephemerista = WalkerDelta(
        time=start_time,
        nsats=24,
        nplanes=3,
        semi_major_axis=29599.8,
        inclination=56.0,
        eccentricity=0.0,
        periapsis_argument=0,
        phasing=1,
        name="galileo",
    )

    compare_against_matlab_json(resources / "constellation" / "galileo_walker_delta_matlab.json", wd_ephemerista)
