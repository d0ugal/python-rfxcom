"""
Protocol Constants
==================

"""

from .base import Packet
from .elec import Elec
from .lighting5 import Lighting5
from .status import Status
from .temphumidity import TempHumidity

#: Write all zeros to reset the RFXtrx
RESET_PACKET = b'\x0D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

#: Packet to request the status from the RFXtrx, this will let us know what
#: modes are enabled and that the device is ready.
STATUS_PACKET = b'\x0D\x00\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'

#: Packet to set the mode for the RFXtrx. The key parts are \x00\x0E\x2F
#: These correlate to a set of 8 bits each which in turn disable or enable
#: an individual protocol. The SDK documentation should be referred to for
#: these or the RFXmngr application can be used to configure the device.
MODE_PACKET = b'\x0D\x00\x00\x01\x03\x53\x00\x00\x0E\x2F\x00\x00\x00\x00'

#: A list containing all the packet types supported in python-rfxcom. The
#: last one is a raw packet and will be used for any unrecognised devices.
HANDLERS = [
    Elec,
    Lighting5,
    Status,
    TempHumidity,
    Packet,  # At the end as we should try it last.
]
