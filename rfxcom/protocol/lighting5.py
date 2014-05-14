"""
Lighting 5
==========

The Lighting 5 packet is used by a number of manufacturers for light control.
For example Lightwave devices use this.

====    ====
Byte    Meaning
====    ====
0       Packet Length, 0x0A (excludes this byte)
1       Packet Type, 0x14
2       Sub Type
3       Sequence Number
4       ID 1
5       ID 2
6       ID 3
7       Unit Code
8       Command
9       Level
10      Filler and RSSI
====    ====

"""

from rfxcom.protocol.base import BasePacketHandler

#: The Packet Types supported by this protocol.
PACKET_TYPES = {
    0x14: "Lighting5"
}

#: The Packet Sub Types for Lighting5
SUB_TYPES = {
    0x00: "LightwaveRF, Siemens",
    0x01: "EMW100 GAO/Everflourish",
    0x02: "BBSB new types",
    0x03: "MDREMOTE LED dimmer",
    0x04: "Conrad RSL2",
    0x05: "Livolo",
    0x06: "RGB TRC02",
}


class Lighting5(BasePacketHandler):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = PACKET_TYPES
        self.SUB_TYPES = SUB_TYPES

    def parse(self, data):
        """Parse a 10 byte packet in the Lighting5 format.

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
        id_ = self.dump_hex(data[4:7])
        unit_code = data[7]
        command = data[8]
        level = data[9]
        rssi = data[10]

        return {
            'packet_length': packet_length,
            'packet_type': packet_type,
            'sequence_number': sequence_number,
            'sub_type': sub_type,
            'sub_type_name': self.SUB_TYPES.get(sub_type),
            'id': id_,
            'unit_code': unit_code,
            'command': command,
            'level': level,
            'rssi': rssi,
        }
