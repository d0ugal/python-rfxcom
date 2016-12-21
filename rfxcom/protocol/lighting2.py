"""
Lighting 5
==========

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


SUB_TYPE_COMMANDS = {
    0x00: {
        0x00: 'Off',
        0x01: 'On',
        0x02: 'Set level',
        0x03: 'Group Off',
        0x04: 'Group On',
        0x05: 'Set Group Level',
    },
    0x01: {
        0x00: "Off",
        0x01: "On",
        0x02: "Learn",
    },
    0x02: {
        0x00: "Off",
        0x01: "On",
        0x02: "Group Off",
        0x03: "Group On",
    }
}

DIM_LEVEL_TO_PERCENT = {
    0x00: 0,
    0x01: 6,
    0x02: 12,
    0x03: 18,
    0x04: 24,
    0x05: 30,
    0x06: 36,
    0x07: 42,
    0x08: 48,
    0x09: 54,
    0x0A: 60,
    0x0B: 66,
    0x0C: 72,
    0x0D: 78,
    0x0E: 84,
    0x0F: 100
    }


class Lighting2(BasePacketHandler):
    """The Lighting2 protocol is a 12 byte packet used by a number of lighting
    systems. For example Lightwave devices use this protocol.

    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x0C (excludes this byte)
    1       Packet Type, 0x11
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       ID 3
    7       ID 4
    8       Unit Code
    9       Command
    10      Dim Level
    11      RSSI and Filler
    ====    ====
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x11: "Lighting2"
        }

        self.PACKET_SUBTYPES = {
            0x00: 'AC',
            0x01: 'HomeEasy EU',
            0x02: 'Anslut'
        }

    def parse(self, data):
        """Parse a 12 byte packet in the Lighting2 format and return a
        dictionary containing the data extracted. An example of a return value
        would be

        .. code-block:: python

            {
                'id': "0x111F342",
                'packet_length': 10,
                'packet_type': 17,
                'sequence_number': 19,
                'sub_type': 0,
                'sub_type_name': "AC",
                'unit_code': 10,
                'command': 1,
                'command_text': "Off",
                'level': 7,
                'rssi': 96,
            }

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        results = self.parse_header_part(data)
        sub_type = results['packet_subtype']

        id_ = self.dump_hex(data[4:8])

        unit_code = data[8]
        command = data[9]
        command_text = SUB_TYPE_COMMANDS.get(sub_type, {}).get(command)
        dim_level = DIM_LEVEL_TO_PERCENT.get(data[10], '--??--')

        sensor_specific = {
            'id': id_,
            'unit_code': unit_code,
            'command': command,
            'command_text': command_text,
            'dim_level': dim_level
        }

        results.update(RfxPacketUtils.parse_signal_upper(data[11]))
        results.update(sensor_specific)

        return results
