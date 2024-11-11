from pydantic import Field

from ephemerista import BaseModel
from ephemerista.comms.antennas import Antenna
from ephemerista.comms.utils import to_db


class Transmitter(BaseModel):
    frequency: float = Field(gt=0.0)
    power: float = Field(gt=0.0)
    line_loss: float = Field(ge=0.0)

    def equivalent_isotropic_radiated_power(self, antenna: Antenna, angle: float) -> float:
        return antenna.gain(self.frequency, angle) + to_db(self.power) - self.line_loss
