from typing import Self
from uuid import uuid4

from pydantic import UUID4, Field

from ephemerista import BaseModel
from ephemerista.comms.antennas import ANTENNA_DISCRIMINATOR, AntennaType
from ephemerista.comms.receiver import ReceiverType
from ephemerista.comms.transmitter import Transmitter
from ephemerista.comms.utils import BOLTZMANN_CONSTANT, free_space_path_loss, to_db


class CommunicationSystem(BaseModel):
    system_id: UUID4 = Field(alias="id", default_factory=uuid4)
    channels: list[UUID4]
    antenna: AntennaType = Field(discriminator=ANTENNA_DISCRIMINATOR)
    receiver: ReceiverType | None = Field(default=None, discriminator="receiver_type")
    transmitter: Transmitter | None = Field(default=None)

    def carrier_to_noise_density(self, rx: Self, losses: float, rng: float, tx_angle: float, rx_angle: float) -> float:
        if not self.transmitter:
            msg = "Transmitter must be defined"
            raise ValueError(msg)
        if not rx.receiver:
            msg = "Receiver must be defined"
            raise ValueError(msg)
        if self.transmitter.frequency != rx.receiver.frequency:
            msg = "Carrier frequencies must match"
            raise ValueError(msg)
        fspl = free_space_path_loss(rng, self.transmitter.frequency)
        eirp = self.transmitter.equivalent_isotropic_radiated_power(self.antenna, tx_angle)
        gt = rx.receiver.gain_to_noise_temperature(rx.antenna, rx_angle)
        return eirp + gt - fspl - losses - to_db(BOLTZMANN_CONSTANT)
