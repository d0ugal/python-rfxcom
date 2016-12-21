
"""
Wind sensors
================

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


class Wind(BasePacketHandler):
    """
    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x10 (excludes this byte)
    1       Packet Type, 0x56
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       Direction High
    7       Direction Low
    8       AV speed High
    9       AV speed Low
    10      Gust High
    11      Gust Low
    12      Temperature High
    13      Temperature Low
    14      Windchill High
    15      Windchill Low
    16      RSSI and Battery Level
    ====    ====


    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x56: "Wind sensors"
        }
        self.PACKET_SUBTYPES = {
            0x01: 'WTGR800',
            0x02: 'WGR800',
            0x03: 'STR918, WGR918, WGR928',
            0x04: 'TFA',
            0x05: 'UPM WDS500',
            0x06: 'WS2300'
        }

    def parse(self, data):
        """Parse a 17 bytes packet in the temp format.

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        results = self.parse_header_part(data)
        sub_type = results['packet_subtype']

        id_ = self.dump_hex(data[4:6])

        direction = data[6] * 256 + data[7]
        if sub_type != 0x05:
            av_speed = (data[8] * 256 + data[9]) * 0.1
        else:
            av_speed = '--??--'
        gust = (data[10] * 256 + data[11]) * 0.1
        if sub_type == 0x04:
            temperature = ((data[12] & 0x7f) * 256 + data[13]) / 10
            signbit = data[12] & 0x80
            if signbit != 0:
                temperature = -temperature
        else:
            temperature = '--??--'
        if sub_type == 0x04:
            wind_chill = ((data[14] & 0x7f) * 256 + data[15]) / 10
            signbit = data[14] & 0x80
            if signbit != 0:
                wind_chill = -wind_chill
        else:
            wind_chill = '--??--'

        sensor_specific = {
            'id': id_,
            'direction': direction,
            'wind_gust': gust
        }
        if av_speed != '--??--':
            sensor_specific['av_speed'] = av_speed
        if temperature != '--??--':
            sensor_specific['temperature'] = temperature
        if wind_chill != '--??--':
            sensor_specific['wind_chill'] = wind_chill

        results.update(RfxPacketUtils.parse_signal_and_battery(data[16]))
        results.update(sensor_specific)

        return results
