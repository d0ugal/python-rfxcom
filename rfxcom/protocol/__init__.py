from .base import Packet
from .elec import Elec
from .status import Status
from .temphumidity import TempHumidity


RESET_PACKET = b'\x0D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
STATUS_PACKET = b'\x0D\x00\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'

HANDLERS = [Elec, Status, TempHumidity, Packet]
