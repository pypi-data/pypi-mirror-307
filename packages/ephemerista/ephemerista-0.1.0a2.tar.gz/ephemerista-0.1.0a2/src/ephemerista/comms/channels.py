from typing import Literal
from uuid import uuid4

from pydantic import UUID4, Field

from ephemerista import BaseModel
from ephemerista.comms.systems import CommunicationSystem
from ephemerista.comms.utils import to_db


class Channel(BaseModel):
    channel_id: UUID4 = Field(alias="id", default_factory=uuid4)
    link_type: Literal["uplink", "downlink"]
    name: str = Field(description="The name of the channel", default="Default Channel")
    data_rate: float
    required_eb_n0: float = Field(json_schema_extra={"title": "Required Eb/N0"})
    margin: float
    modulation: Literal["BPSK", "QPSK", "8PSK", "16QAM", "32QAM", "64QAM", "128QAM", "256QAM"]
    roll_off: float = Field(default=1.5)
    forward_error_correction: float = Field(default=0.5)

    def bits_per_symbol(self) -> int:
        return {
            "BPSK": 1,
            "QPSK": 2,
            "8PSK": 3,
            "16QAM": 4,
            "32QAM": 5,
            "64QAM": 6,
            "128QAM": 7,
            "256QAM": 8,
        }[self.modulation]

    @property
    def bandwidth(self) -> float:
        return self.data_rate * (1 + self.roll_off) / self.bits_per_symbol() / self.forward_error_correction

    def bit_energy_to_noise_density(
        self,
        tx: CommunicationSystem,
        rx: CommunicationSystem,
        losses: float,
        rng: float,
        tx_angle: float,
        rx_angle: float,
    ) -> float:
        if self.channel_id not in tx.channels:
            msg = "Channel not supported by transmitter"
            raise ValueError(msg)
        if self.channel_id not in rx.channels:
            msg = "Channel not supported by receiver"
            raise ValueError(msg)

        c_n0 = tx.carrier_to_noise_density(rx, losses, rng, tx_angle, rx_angle)
        return c_n0 - to_db(self.data_rate)
