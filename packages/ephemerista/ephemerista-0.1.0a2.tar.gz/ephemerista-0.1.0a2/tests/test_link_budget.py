import pytest

from ephemerista.analysis.link_budget import LinkBudget, LinkBudgetResults
from ephemerista.angles import Angle
from ephemerista.assets import Asset, GroundStation, Spacecraft
from ephemerista.comms.antennas import FieldOfRegard, SimpleAntenna
from ephemerista.comms.channels import Channel
from ephemerista.comms.receiver import SimpleReceiver
from ephemerista.comms.systems import CommunicationSystem
from ephemerista.comms.transmitter import Transmitter
from ephemerista.comms.utils import free_space_path_loss
from ephemerista.propagators.sgp4 import SGP4
from ephemerista.scenarios import Scenario
from ephemerista.time import TimeDelta

tle = """
1 99878U 14900A   24103.76319466  .00000000  00000-0 -11394-2 0    01
2 99878  97.5138 156.7457 0016734 205.2381 161.2435 15.13998005    06
"""

uplink = Channel(link_type="uplink", modulation="BPSK", data_rate=430502, required_eb_n0=2.3, margin=3)
downlink = Channel(link_type="downlink", modulation="BPSK", data_rate=861004, required_eb_n0=4.2, margin=3)

slant_range = 2192.92  # km
frequency = 2308e6  # Hz

gs_antenna = SimpleAntenna(
    gain_db=30, beamwidth_deg=5, field_of_regard=FieldOfRegard(degrees=90), design_frequency=frequency
)
gs_transmitter = Transmitter(power=4, frequency=frequency, line_loss=1.0)
gs_receiver = SimpleReceiver(system_noise_temperature=889, frequency=frequency)
gs_system = CommunicationSystem(
    channels=[uplink.channel_id, downlink.channel_id],
    transmitter=gs_transmitter,
    receiver=gs_receiver,
    antenna=gs_antenna,
)

sc_antenna = SimpleAntenna(gain_db=6.5, beamwidth_deg=60, design_frequency=frequency)
sc_transmitter = Transmitter(power=1.348, frequency=frequency, line_loss=1.0)
sc_receiver = SimpleReceiver(system_noise_temperature=429, frequency=frequency)
sc_system = CommunicationSystem(
    channels=[uplink.channel_id, downlink.channel_id],
    transmitter=sc_transmitter,
    receiver=sc_receiver,
    antenna=sc_antenna,
)

station_coordinates = [
    (38.017, 23.731),
    (36.971, 22.141),
    (35.501, 24.011),
    (39.326, -82.101),
    (50.750, 6.211),
]

stations = [
    Asset(
        model=GroundStation.from_lla(longitude, latitude, minimum_elevation=Angle.from_degrees(10)),
        name=f"Station {i}",
        comms=[gs_system],
    )
    for i, (latitude, longitude) in enumerate(station_coordinates)
]

propagator = SGP4(tle=tle)
sc = Asset(model=Spacecraft(propagator=propagator), name="PHASMA", comms=[sc_system])

start_date = propagator.time
end_date = start_date + TimeDelta.from_days(1)

scenario = Scenario(
    assets=[*stations, sc],
    channels=[uplink, downlink],
    name="PHASMA Link Budget",
    start_time=start_date,
    end_time=end_date,
)


def test_fspl():
    assert free_space_path_loss(slant_range, frequency) == pytest.approx(166, rel=1e-1)


def test_gs_transmitter():
    assert gs_transmitter.equivalent_isotropic_radiated_power(gs_antenna, 0.0) == pytest.approx(35.0, rel=1e-1)


def test_gs_receiver():
    expected = -4.99 + 3 + 1.5 + 1
    assert gs_receiver.gain_to_noise_temperature(gs_antenna, 0.0) == pytest.approx(expected, rel=1e-1)


def test_sc_transmitter():
    assert sc_transmitter.equivalent_isotropic_radiated_power(sc_antenna, 0.0) == pytest.approx(7.5, rel=1e-1)


def test_sc_receiver():
    assert sc_receiver.gain_to_noise_temperature(sc_antenna, 0.0) == pytest.approx(-19.82, rel=1e-1)


def test_uplink():
    ebn0 = uplink.bit_energy_to_noise_density(gs_system, sc_system, 8.5, slant_range, 0.0, 0.0)
    assert ebn0 == pytest.approx(10, rel=1.0)


def test_downlink():
    ebn0 = downlink.bit_energy_to_noise_density(sc_system, gs_system, 8.5, slant_range, 0.0, 0.0)
    assert ebn0 == pytest.approx(1.5, rel=1e-1)


def test_link_budget():
    lb = LinkBudget(scenario=scenario)
    results = lb.analyze()
    assert isinstance(results, LinkBudgetResults)
