"""
Energy Usage Sensors
====================

"""

from rfxcom.protocol.base import BasePacketHandler


class Elec(BasePacketHandler):
    """The Elec protocol is a 17 byte packet used by energy sensors. The
    sensors transmit this packet periodically and the key data it provides is
    the current watt usage and total watt usage. It is used for example by the
    Owl energy monitors.

    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x11 (excludes this byte)
    1       Packet Type, 0x5A
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       Count (?)
    7       Current Watts 1
    8       Current Watts 2
    9       Current Watts 3
    10      Current Watts 4
    11      Total Watts 1
    12      Total Watts 2
    13      Total Watts 3
    14      Total Watts 4
    15      Total Watts 5
    16      Total Watts 6
    17      Battery Level and RSSI
    ====    ====
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x5A: "Energy usage sensors"
        }
        self.SUB_TYPES = {
            0x01: "CM119/160",
            0x02: "CM180",
        }

    def _bytes_to_uint_32(self, bytes_):
        """Converts an array of 4 bytes to a 32bit integer.

        :param data: bytearray to be converted to a 32bit integer
        :type data: bytearray

        :return: the integer
        :rtype: int
        """
        return ((bytes_[0] * pow(2, 24)) +
                (bytes_[1] << 16) + (bytes_[2] << 8) + bytes_[3])

    def _bytes_to_uint_48(self, bytes_):
        """Converts an array of 6 bytes to a 48bit integer.

        :param data: bytearray to be converted to a 48bit integer
        :type data: bytearray

        :return: the integer
        :rtype: int
        """
        return ((bytes_[0] * pow(2, 40)) + (bytes_[1] * pow(2, 32)) +
                (bytes_[2] * pow(2, 24)) + (bytes_[3] << 16) +
                (bytes_[4] << 8) + bytes_[4])

    def parse(self, data):
        """Parse the packet and return a dictionary with the following format.

        .. code-block:: python

            {
                'count': 3,
                'current_watts': 692,
                'id': "0x2EB2",
                'packet_length': 17,
                'packet_type': 90,
                'sequence_number': 0,
                'sub_type': 1,
                'sub_type_name': "CM119/160",
                'total_watts': 920825.1947099693,
            }

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        TOTAL_DIVISOR = 223.666

        packet_length = data[0]
        packet_type = data[1]
        sub_type = data[2]
        sequence_number = data[3]
        id_ = self.dump_hex(data[4:6])
        count = data[6]
        instant = data[7:11]
        total = data[11:16]

        current_watts = self._bytes_to_uint_32(instant)
        total_watts = self._bytes_to_uint_48(total) / TOTAL_DIVISOR

        return {
            'count': count,
            'current_watts': current_watts,
            'id': id_,
            'packet_length': packet_length,
            'packet_type': packet_type,
            'packet_type_name': self.PACKET_TYPES.get(packet_type),
            'sequence_number': sequence_number,
            'sub_type': sub_type,
            'sub_type_name': self.SUB_TYPES.get(sub_type),
            'total_watts': total_watts,
        }
