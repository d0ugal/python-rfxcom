"""
Lighting 5
==========

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


SUB_TYPE_COMMANDS = {
    0x00: {
        0x00: "Off",
        0x01: "On",
        0x02: "Group Off",
        0x03: "mood1",
        0x04: "mood2",
        0x05: "mood3",
        0x06: "mood4",
        0x07: "mood5",
        0x08: "reserved",
        0x09: "reserved",
        0x0A: "unlock",
        0x0B: "lock",
        0x0C: "all lock",
        0x0D: "close (inline relay)",
        0x0E: "stop (inline relay)",
        0x0F: "open (inline relay)",
        0x10: "set level",
        0x11: "colour Palette",
        0x12: "Colour Tone",
        0x13: "Colour Cycle",
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
    },
    0x03: {
        0x00: "Power",
        0x01: "Light",
        0x02: "Bright",
        0x03: "dim",
        0x04: "100%",
        0x05: "50%",
        0x06: "25%",
        0x07: "Mode+",
        0x08: "Speed-",
        0x09: "Speed+",
        0x0A: "Mode-",
    },
    0x04: {
        0x00: "Off",
        0x01: "On",
        0x02: "Group Off",
        0x03: "Group On",
    },
    0x05: {
        0x00: "Group Off",
        0x01: "On/Off dinner or Gang1",
        0x02: "Dim+ or Gang2 on/off",
        0x03: "Dim- or Gang3 on/off",
    },
    0x06: {
        0x00: "Off",
        0x01: "On",
        0x02: "Bright",
        0x03: "Dim",
        0x04: "Colour+",
        0x05: "Colour-",
        0x06: "Select color",
    },
}


class Lighting5(BasePacketHandler):
    """The Lighting5 protocol is a 10 byte packet used by a number of lighting
    systems. For example Lightwave devices use this protocol.

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
    10      RSSI and Filler
    ====    ====
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x14: "Lighting5"
        }

        self.PACKET_SUBTYPES = {
            0x00: "LightwaveRF, Siemens",
            0x01: "EMW100 GAO/Everflourish",
            0x02: "BBSB new types",
            0x03: "MDREMOTE LED dimmer",
            0x04: "Conrad RSL2",
            0x05: "Livolo",
            0x06: "RGB TRC02",
        }

    def parse(self, data):
        """Parse a 10 byte packet in the Lighting5 format and return a
        dictionary containing the data extracted. An example of a return value
        would be

        .. code-block:: python

            {
                'id': "0xF394AB",
                'packet_length': 10,
                'packet_type': 20,
                'sequence_number': 173,
                'sub_type': 0,
                'sub_type_name': "LightwaveRF, Siemens",
                'unit_code': 1,
                'command': 1,
                'command_text': "On",
                'level': 0,
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

        id_ = self.dump_hex(data[4:7])
        unit_code = data[7]
        command = data[8]
        command_text = SUB_TYPE_COMMANDS.get(sub_type, {}).get(command)
        level = data[9]

        sensor_specific = {
            'id': id_,
            'unit_code': unit_code,
            'command': command,
            'command_text': command_text,
            'level': level
        }

        results.update(RfxPacketUtils.parse_signal_upper(data[10]))
        results.update(sensor_specific)

        return results
