"""
UV sensors
================

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


class UltraViolet(BasePacketHandler):
    """
    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x09 (excludes this byte)
    1       Packet Type, 0x57
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       UV
    7       Temperature High
    8       Temperature Low
    9       RSSI and Battery Level
    ====    ====


    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x57: "UV sensors"
        }
        self.PACKET_SUBTYPES = {
            0x01: 'UVN128, UV138',
            0x02: 'UVN800',
            0x03: 'TFA'
        }

    def parse(self, data):
        """Parse a 10 bytes packet in the UltraViolet format and return a
        dictionary containing the data extracted. An example of a return value
        would be:

        .. code-block:: python

            {
                'id': "0x2EB2",
                'packet_length': 9,
                'packet_type': 87,
                'packet_type_name': 'UV sensors',
                'sequence_number': 0,
                'packet_subtype': 3,
                'packet_subtype_name': "TFA",
                'temperature': 21.3,
                'uv': 3,
                'signal_level': 9,
                'battery_level': 6,
            }

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        id_ = self.dump_hex(data[4:6])

        uv = data[6]
        temperature = ((data[7] & 0x7f) * 256 + data[8]) / 10
        signbit = data[7] & 0x80
        if signbit != 0:
            temperature = -temperature

        results = self.parse_header_part(data)
        sub_type = results['packet_subtype']

        sensor_specific = {
            'id': id_,
            'uv': uv
        }
        if sub_type == 0x03:
            sensor_specific['temperature'] = temperature

        results.update(RfxPacketUtils.parse_signal_and_battery(data[9]))
        results.update(sensor_specific)

        return results
