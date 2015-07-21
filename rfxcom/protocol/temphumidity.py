"""
Temperature and Humidity sensors
================================

"""

from rfxcom.protocol.base import BasePacketHandler


class TempHumidity(BasePacketHandler):
    """
    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x0A (excludes this byte)
    1       Packet Type, 0x14
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       Temperature High (7 bits), Temperature sign (1 bit)
    7       Temperature Low
    8       Humidity
    9       Humidity Status
    10      Battery Level and RSSI
    ====    ====


    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x52: "Temperature and humidity sensors"
        }
        self.SUB_TYPES = {
            0x01: 'THGN122/123, THGN132, THGR122/228/238/268',
            0x02: 'THGR810, THGN800, THGR810',
            0x03: 'RTGR328',
            0x04: 'THGR328',
            0x05: 'WTGR800',
            0x06: 'THGR918/928, THGRN228, THGN500',
            0x07: 'TFA TS34C, Cresta',
            0x08: 'WT260,WT260H,WT440H,WT450,WT450H',
            0x09: 'Viking 02035,02038 (02035 has no humidity)',
            0x0A: 'Rubicson',
            0x0B: 'EW109',
        }

    def parse(self, data):
        """Parse a 10 byte packet in the temp format.

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        packet_length = data[0]
        packet_type = data[1]
        sub_type = data[2]
        sequence_number = data[3]
        id_ = self.dump_hex(data[4:6])

        temperature = ((data[6] & 0x7f) * 256 + data[7]) / 10
        signbit = data[6] & 0x80
        if signbit != 0:
            temperature = -temperature
        humidity = data[8]
        humidity_status = data[9]
        battery_signal_level = data[10]
        rssi = data[10]

        return {
            'packet_length': packet_length,
            'packet_type': packet_type,
            'packet_type_name': self.PACKET_TYPES.get(packet_type),
            'sequence_number': sequence_number,
            'sub_type': sub_type,
            'sub_type_name': self.SUB_TYPES.get(sub_type),
            'id': id_,
            'temperature': temperature,
            'humidity': humidity,
            'humidity_status': humidity_status,
            'battery_signal_level': battery_signal_level,
            'signal_strength': rssi,
        }
