"""
Rain sensors
================

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


class Rain(BasePacketHandler):
    """
    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x0A (excludes this byte)
    1       Packet Type, 0x55
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       Rain Rate High
    7       Rain Rate Low
    8       Rain Total High
    9       Rain total Medium
    10      Rain Total Low
    11      RSSI and Battery Level
    ====    ====

    Rain Rate unit is mm/hour
    Rain Total is mm

    Note:
    need example data to implement correctly subtype 6 (La Crosse TX5)
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x55: "Rain sensors"
        }
        self.PACKET_SUBTYPES = {
            0x01: 'RGR126/682/918',
            0x02: 'PCR800',
            0x03: 'TFA',
            0x04: 'UPM RG700',
            0x05: 'WS2300',
            0x06: 'La Crosse TX5'
        }

    def parse(self, data):
        """Parse a 12 bytes packet in the temp format.

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        results = self.parse_header_part(data)
        sub_type = results['packet_subtype']

        id_ = self.dump_hex(data[4:6])

        rain_rate_high = data[6]
        rain_rate_low = data[7]
        if sub_type == 0x01:
            rain_rate = rain_rate_high * 0x100 + rain_rate_low
        elif sub_type == 0x02:
            rain_rate = float(rain_rate_high * 0x100 + rain_rate_low) / 100
        else:
            rain_rate = '--??--'
        rain_total1 = data[8]
        rain_total2 = data[9]
        rain_total3 = data[10]
        if sub_type != 0x06:
            rain_total = float(
                rain_total1 * 0x1000 + rain_total2 * 0x100 + rain_total3) / 10
        else:
            rain_total = '--??--'

        sensor_specific = {
            'id': id_
        }
        if rain_rate != '--??--':
            sensor_specific['rain_rate'] = rain_rate
        if rain_total != '--??--':
            sensor_specific['rain_total'] = rain_total

        results.update(RfxPacketUtils.parse_signal_and_battery(data[11]))
        results.update(sensor_specific)

        return results
