from functools import partial
from typing import Literal, Self

import lox_space as lox
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pydantic import UUID4, Field

from ephemerista import BaseModel
from ephemerista.analysis import Analysis
from ephemerista.analysis.visibility import Pass, Visibility, VisibilityResults, Window
from ephemerista.angles import Angle
from ephemerista.assets import AssetKey, GroundStation, Spacecraft, asset_id
from ephemerista.comms.channels import Channel
from ephemerista.comms.systems import CommunicationSystem
from ephemerista.comms.utils import free_space_path_loss
from ephemerista.coords.trajectories import Trajectory
from ephemerista.scenarios import Ensemble, Scenario
from ephemerista.time import Time, TimeDelta


class LinkStats(BaseModel):
    slant_range: float
    fspl: float
    tx_angle: Angle
    rx_angle: Angle
    eirp: float
    gt: float
    c_n0: float
    eb_n0: float
    margin: float
    losses: float
    data_rate: float
    bandwidth: float

    @classmethod
    def calculate(
        cls,
        time: Time,
        gs_pass: Pass,
        channel: Channel,
        link_type: Literal["uplink", "downlink"],
        target: Spacecraft,
        observer: GroundStation,
        target_tra: Trajectory,
        observer_tra: Trajectory,
        target_comms: CommunicationSystem,
        observer_comms: CommunicationSystem,
        losses: float,
    ) -> Self:
        sc_state = target_tra.interpolate(time)
        gs_state = observer_tra.interpolate(time)
        sc_angle = target.off_boresight_angle(sc_state, gs_state, target_comms)
        elevation = gs_pass.interpolate(time).elevation.radians
        gs_angle = observer.off_boresight_angle(elevation, observer_comms)
        slant_range = float(np.linalg.norm(sc_state.position - gs_state.position))
        if link_type == "uplink":
            rx_angle = sc_angle
            tx_angle = gs_angle
            rx = target_comms
            tx = observer_comms
        else:
            rx_angle = gs_angle
            tx_angle = sc_angle
            rx = observer_comms
            tx = target_comms
        if not tx.transmitter:
            msg = "Transmitter not found"
            raise ValueError(msg)
        if not rx.receiver:
            msg = "Receiver not found"
            raise ValueError(msg)
        fspl = free_space_path_loss(slant_range, tx.transmitter.frequency)
        eirp = tx.transmitter.equivalent_isotropic_radiated_power(tx.antenna, tx_angle)
        gt = rx.receiver.gain_to_noise_temperature(rx.antenna, rx_angle)
        c_n0 = tx.carrier_to_noise_density(rx, losses, slant_range, tx_angle, rx_angle)
        eb_n0 = channel.bit_energy_to_noise_density(tx, rx, losses, slant_range, tx_angle, rx_angle)
        margin = eb_n0 - channel.required_eb_n0 - channel.margin
        return cls(
            slant_range=slant_range,
            fspl=fspl,
            tx_angle=Angle.from_radians(tx_angle),
            rx_angle=Angle.from_radians(rx_angle),
            eirp=eirp,
            gt=gt,
            c_n0=c_n0,
            eb_n0=eb_n0,
            margin=margin,
            losses=losses,
            data_rate=channel.data_rate,
            bandwidth=channel.bandwidth,
        )


class Link(BaseModel):
    window: Window
    link_type: Literal["uplink", "downlink"]
    times: list[Time]
    stats: list[LinkStats]

    def plot(self):
        dts = [t.datetime for t in self.times]
        slant_range = [s.slant_range for s in self.stats]
        tx_angle = [s.tx_angle.degrees for s in self.stats]
        rx_angle = [s.rx_angle.degrees for s in self.stats]
        fspl = [s.fspl for s in self.stats]
        eirp = [s.eirp for s in self.stats]
        gt = [s.gt for s in self.stats]
        losses = [s.losses for s in self.stats]
        c_n0 = [s.c_n0 for s in self.stats]
        eb_n0 = [s.eb_n0 for s in self.stats]
        margin = [s.margin for s in self.stats]

        fig, ax = plt.subplots(3, 3, figsize=(12, 8))
        plt.subplots_adjust(hspace=0.4, wspace=0.4)

        fig.suptitle(f"{self.link_type.title()} from {self.window.start.to_utc()} to {self.window.stop.to_utc()}")

        for a in ax.flat:
            a.xaxis.set_major_locator(mdates.HourLocator())
            a.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            a.xaxis.set_tick_params(rotation=45)
            a.grid()

        ax[0, 0].plot(dts, slant_range)
        ax[0, 0].set_title("Slant Range")
        ax[0, 0].set_ylabel("km")

        ax[0, 1].plot(dts, tx_angle)
        ax[0, 1].plot(dts, rx_angle)
        ax[0, 1].set_title("Off Boresight Angles")
        ax[0, 1].set_ylabel("degrees")

        ax[0, 2].plot(dts, fspl)
        ax[0, 2].set_title("Free Space Path Loss")
        ax[0, 2].set_ylabel("dB")

        ax[1, 0].plot(dts, eirp)
        ax[1, 0].set_title("EIRP")
        ax[1, 0].set_ylabel("dBW")

        ax[1, 1].plot(dts, gt)
        ax[1, 1].set_title("G/T")
        ax[1, 1].set_ylabel("dB/K")

        ax[1, 2].plot(dts, losses)
        ax[1, 2].set_title("Losses")
        ax[1, 2].set_ylabel("dB")

        ax[2, 0].plot(dts, c_n0)
        ax[2, 0].set_title("C/N0")
        ax[2, 0].set_ylabel("dB")

        ax[2, 1].plot(dts, eb_n0)
        ax[2, 1].set_title("Eb/N0")
        ax[2, 1].set_ylabel("dB")

        ax[2, 2].plot(dts, margin)
        ax[2, 2].set_title("Link Margin")
        ax[2, 2].set_ylabel("dB")


class LinkBudgetResults(BaseModel):
    links: dict[UUID4, dict[UUID4, list[Link]]]

    def get(self, observer: AssetKey, target: AssetKey) -> list[Link]:
        target_passes = self.links.get(asset_id(target), {})
        return target_passes.get(asset_id(observer), [])

    def __getitem__(self, key: tuple[AssetKey, AssetKey]) -> list[Link]:
        return self.get(*key)

    def to_dataframe(self, observer: AssetKey, target: AssetKey) -> pd.DataFrame:
        links = self.get(observer, target)
        data = []
        for link in links:
            slant_range = np.mean([s.slant_range for s in link.stats])
            tx_angle = np.mean([s.tx_angle.degrees for s in link.stats])
            rx_angle = np.mean([s.rx_angle.degrees for s in link.stats])
            fspl = np.mean([s.fspl for s in link.stats])
            eirp = np.mean([s.eirp for s in link.stats])
            gt = np.mean([s.gt for s in link.stats])
            losses = np.mean([s.losses for s in link.stats])
            c_n0 = np.mean([s.c_n0 for s in link.stats])
            eb_n0 = np.mean([s.eb_n0 for s in link.stats])
            margin = np.mean([s.margin for s in link.stats])
            data.append(
                {
                    "start": link.window.start.datetime,
                    "end": link.window.stop.datetime,
                    "duration": link.window.duration,
                    "type": link.link_type,
                    "mean_slant_range": slant_range,
                    "mean_tx_angle": tx_angle,
                    "mean_rx_angle": rx_angle,
                    "mean_fspl": fspl,
                    "mean_eirp": eirp,
                    "mean_gt": gt,
                    "mean_losses": losses,
                    "mean_c_n0": c_n0,
                    "mean_eb_n0": eb_n0,
                    "mean_margin": margin,
                }
            )
        return pd.DataFrame(data)


class LinkBudget(Analysis[LinkBudgetResults]):
    scenario: Scenario
    start_time: Time | None = Field(default=None)
    end_time: Time | None = Field(default=None)

    def analyze(
        self,
        ensemble: Ensemble | None = None,
        visibility: VisibilityResults | None = None,
    ) -> LinkBudgetResults:
        if not ensemble:
            ensemble = self.scenario.propagate()

        if not visibility:
            visibility = Visibility(scenario=self.scenario, start_time=self.start_time, end_time=self.end_time).analyze(
                ensemble
            )

        # start_time = self.start_time or self.scenario.start_date
        # end_time = self.end_time or self.scenario.end_date

        links = {}

        for target_id, observers in visibility.passes.items():
            target = self.scenario[target_id]
            if not isinstance(target.model, Spacecraft):
                continue
            target_tra = ensemble[target]
            target_channels = set()
            for c in target.comms:
                target_channels.update(c.channels)

            if target_id not in links:
                links[target_id] = {}

            for observer_id, passes in observers.items():
                links[target_id][observer_id] = []

                observer = self.scenario[observer_id]
                if not isinstance(observer.model, GroundStation):
                    continue
                observer_tra = ensemble[observer]
                observer_channels = set()
                for c in observer.comms:
                    observer_channels.update(c.channels)

                channels = target_channels.intersection(observer_channels)
                if not channels:
                    continue

                for channel_id in channels:
                    channel = self.scenario.channel_by_id(channel_id)
                    link_type = channel.link_type
                    target_comms = target.comms_by_channel_id(channel_id)
                    observer_comms = observer.comms_by_channel_id(channel_id)

                    if link_type == "uplink":
                        rx = target_comms
                        tx = observer_comms
                    else:
                        rx = observer_comms
                        tx = target_comms

                    if not rx.receiver or not tx.transmitter:
                        continue

                    for gs_pass in passes:
                        t0 = gs_pass.window.start
                        t1 = gs_pass.window.stop
                        times = [float(t - t0) for t in gs_pass.times]
                        func = partial(
                            lambda t,
                            gs_pass,
                            channel,
                            link_type,
                            target,
                            observer,
                            target_tra,
                            observer_tra,
                            target_comms,
                            observer_comms,
                            losses: viability(
                                t,
                                gs_pass=gs_pass,
                                channel=channel,
                                link_type=link_type,
                                target=target.model,
                                observer=observer.model,
                                target_tra=target_tra,
                                observer_tra=observer_tra,
                                target_comms=target_comms,
                                observer_comms=observer_comms,
                                losses=losses,
                            ),
                            gs_pass=gs_pass,
                            channel=channel,
                            link_type=link_type,
                            target=target,
                            observer=observer,
                            target_tra=target_tra,
                            observer_tra=observer_tra,
                            target_comms=target_comms,
                            observer_comms=observer_comms,
                            losses=0.0,
                        )

                        windows = lox.find_windows(
                            func,
                            t0._time,
                            t1._time,
                            times,
                        )

                        for w in windows:
                            window = Window._from_lox(w)
                            times = window.start.trange(window.stop, self.scenario.time_step)
                            stats = [
                                LinkStats.calculate(
                                    t,
                                    gs_pass,
                                    channel,
                                    link_type,
                                    target.model,
                                    observer.model,
                                    target_tra,
                                    observer_tra,
                                    target_comms,
                                    observer_comms,
                                    0.0,
                                )
                                for t in times
                            ]
                            links[target_id][observer_id].append(
                                Link(window=window, link_type=link_type, stats=stats, times=times)
                            )

        return LinkBudgetResults(links=links)


def viability(
    t: float,
    *,
    gs_pass: Pass,
    channel: Channel,
    link_type: Literal["uplink", "downlink"],
    target: Spacecraft,
    observer: GroundStation,
    target_tra: Trajectory,
    observer_tra: Trajectory,
    target_comms: CommunicationSystem,
    observer_comms: CommunicationSystem,
    losses: float,
) -> float:
    time = gs_pass.window.start + TimeDelta(t)
    sc_state = target_tra.interpolate(time)
    gs_state = observer_tra.interpolate(time)
    sc_angle = target.off_boresight_angle(sc_state, gs_state, target_comms)
    elevation = gs_pass.interpolate(time).elevation.radians
    gs_angle = observer.off_boresight_angle(elevation, observer_comms)
    slant_range = float(np.linalg.norm(sc_state.position - gs_state.position))
    if link_type == "uplink":
        rx_angle = sc_angle
        tx_angle = gs_angle
        rx = target_comms
        tx = observer_comms
    else:
        rx_angle = gs_angle
        tx_angle = sc_angle
        rx = observer_comms
        tx = target_comms
    if not tx.transmitter:
        msg = "Transmitter not found"
        raise ValueError(msg)
    if not rx.receiver:
        msg = "Receiver not found"
        raise ValueError
    val = (
        channel.bit_energy_to_noise_density(tx, rx, losses, slant_range, tx_angle, rx_angle)
        - channel.required_eb_n0
        - channel.margin
    )

    return val
