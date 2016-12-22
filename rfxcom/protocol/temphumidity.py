"""
Temperature and Humidity sensors
================================

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


class TempHumidity(BasePacketHandler):
    """
    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x0A (excludes this byte)
    1       Packet Type, 0x52
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       Temperature High (7 bits), Temperature sign (1 bit)
    7       Temperature Low
    8       Humidity
    9       Humidity Status
    10      RSSI and Battery Level
    ====    ====


    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x52: "Temperature and humidity sensors"
        }
        self.PACKET_SUBTYPES = {
            0x01: 'THGN122/123, THGN132, THGR122/228/238/268',
            0x02: 'THGR810, THGN801, THGN800',
            0x03: 'RTGR328',
            0x04: 'THGR328',
            0x05: 'WTGR800',
            0x06: 'THGR918/928, THGRN228, THGN500',
            0x07: 'TFA TS34C, Cresta',
            0x08: 'WT260,WT260H,WT440H,WT450,WT450H',
            0x09: 'Viking 02035,02038 (02035 has no humidity)',
            0x0A: 'Rubicson',
            0x0B: 'EW109',
            0x0C: 'Imagintronix Soil Sensor'
        }

    def parse(self, data):
        """Parse a 11 bytes packet in the TemperatureHumidity format and return a
        dictionary containing the data extracted. An example of a return value
        would be:

        .. code-block:: python

            {
                'id': "0x2EB2",
                'packet_length': 10,
                'packet_type': 82,
                'packet_type_name': 'Temperature and humidity sensors',
                'sequence_number': 0,
                'packet_subtype': 2,
                'packet_subtype_name': "THGR810, THGN801, THGN800",
                'temperature': 21.3,
                'humidity': 91,
                'humidity_status': "Wet"
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
        channel = data[5]

        temperature = ((data[6] & 0x7f) * 256 + data[7]) / 10
        signbit = data[6] & 0x80
        if signbit != 0:
            temperature = -temperature
        humidity = data[8]
        humidity_status = self._extract_humidity_status(data[9])

        sensor_specific = {
            'id': id_,
            'channel': channel,
            'temperature': temperature,
            'humidity': humidity,
            'humidity_status': humidity_status
        }

        results = self.parse_header_part(data)
        results.update(RfxPacketUtils.parse_signal_and_battery(data[10]))
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
