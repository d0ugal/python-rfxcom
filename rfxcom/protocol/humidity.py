"""
Humidity sensors
================

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


class Humidity(BasePacketHandler):
    """
    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x08 (excludes this byte)
    1       Packet Type, 0x51
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       Humidity
    7       Humidity Status
    8       RSSI and Battery Level
    ====    ====


    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x51: "Humidity sensors"
        }
        self.PACKET_SUBTYPES = {
            0x01: 'LaCrosse TX3',
            0x02: 'LaCrosse WS2300'
        }

    def parse(self, data):
        """Parse a 9 bytes packet in the temp format.

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        id_ = self.dump_hex(data[4:6])
        # channel = data[5] TBC

        humidity = data[6]
        humidity_status = self._extract_humidity_status(data[7])

        sensor_specific = {
            'id': id_,
            # 'channel': channel, TBC
            'humidity': humidity,
            'humidity_status': humidity_status
        }

        results = self.parse_header_part(data)
        results.update(RfxPacketUtils.parse_signal_and_battery(data[8]))
        results.update(sensor_specific)

        return results

    def _extract_humidity_status(self, data):
        """Extract the humidity status.

        :param data: byte to be parsed
        :type data: byte

        :return: String containing the human readable status
        :rtype: string
        """
        if data == 0x00:
            return "Dry"
        elif data == 0x01:
            return "Comfort"
        elif data == 0x02:
            return "Normal"
        elif data == 0x03:
            return "Wet"
        else:
            return "--??--"
