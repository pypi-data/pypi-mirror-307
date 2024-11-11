import abc
from typing import Literal

from pydantic import Field

from ephemerista import BaseModel
from ephemerista.comms.antennas import Antenna
from ephemerista.comms.utils import ROOM_TEMPERATURE, from_db, to_db

DISCRIMINATOR = "receiver_type"


class Receiver(BaseModel, abc.ABC):
    frequency: float = Field(gt=0.0)

    @abc.abstractmethod
    def gain_to_noise_temperature(self, antenna: Antenna, angle: float) -> float:
        raise NotImplementedError()


class SimpleReceiver(Receiver):
    receiver_type: Literal["simple"] = Field(default="simple", alias="type", repr=False, frozen=True)
    system_noise_temperature: float = Field(gt=0.0)

    def gain_to_noise_temperature(self, antenna: Antenna, angle: float) -> float:
        return antenna.gain(self.frequency, angle) - to_db(self.system_noise_temperature)


class ComplexReceiver(Receiver):
    receiver_type: Literal["complex"] = Field(default="complex", alias="type", repr=False, frozen=True)
    antenna_noise_temperature: float = Field(gt=0.0, default=265)
    lna_gain: float = Field(gt=0.0)
    lna_noise_figure: float = Field(ge=0.0)
    noise_figure: float = Field(ge=0.0)
    loss: float = Field(ge=0.0)

    def noise_temperature(self) -> float:
        return ROOM_TEMPERATURE * (10 ** (self.noise_figure / 10) - 1)

    def system_noise_temperature(self) -> float:
        loss = from_db(-self.loss)
        return self.antenna_noise_temperature * loss + ROOM_TEMPERATURE * (1 - loss) + self.noise_temperature()

    def gain_to_noise_temperature(self, antenna: Antenna, angle: float) -> float:
        t_sys = self.system_noise_temperature()
        return antenna.gain(self.frequency, angle) - to_db(t_sys) + self.lna_gain - self.lna_noise_figure - self.loss


type ReceiverType = SimpleReceiver | ComplexReceiver
