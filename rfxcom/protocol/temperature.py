"""
Temperature sensors
===================

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


class Temperature(BasePacketHandler):
    """
    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x08 (excludes this byte)
    1       Packet Type, 0x50
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       Temperature High (7 bits), Temperature sign (1 bit)
    7       Temperature Low
    8       RSSI and Battery Level
    ====    ====


    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x50: "Temperature sensors"
        }
        self.PACKET_SUBTYPES = {
            0x01: 'THR128/138, THC138',
            0x02: 'THC238/268,THN132,THWR288,THRN122,THN122,AW129/131',
            0x03: 'THWR800',
            0x04: 'RTHN318',
            0x05: 'La Crosse TX2, TX3, TX4, TX17',
            0x06: 'TS15C',
            0x07: 'Viking 02811',
            0x08: 'La Crosse WS2300',
            0x09: 'RUBiCSON',
            0x0A: 'TFA 30.3133'
        }

    def parse(self, data):
        """Parse a 9 bytes packet in the Temperature format and return a
        dictionary containing the data extracted. An example of a return value
        would be:

        .. code-block:: python

            {
                'id': "0x2EB2",
                'packet_length': 8,
                'packet_type': 80,
                'packet_type_name': 'Temperature sensors',
                'sequence_number': 0,
                'packet_subtype': 1,
                'packet_subtype_name': "THR128/138, THC138",
                'temperature': 21.3,
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
        # channel = data[5] TBC

        temperature = ((data[6] & 0x7f) * 256 + data[7]) / 10
        signbit = data[6] & 0x80
        if signbit != 0:
            temperature = -temperature

        sensor_specific = {
            'id': id_,
            # 'channel': channel, TBC
            'temperature': temperature
        }

        results = self.parse_header_part(data)
        results.update(RfxPacketUtils.parse_signal_and_battery(data[8]))
        results.update(sensor_specific)

        return results
