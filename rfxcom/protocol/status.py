from rfxcom.protocol.base import BasePacketHandler


class Status(BasePacketHandler):

    def __init__(self):

        super(Status, self).__init__()

        self.PACKET_TYPES = {
            0x01: "Interface message"
        }

        self.SUB_TYPES = {
            0x00: "Response on a mode command",
            0xFF: "Wrong command recieved from the application.",
        }

    def parse(self, data):
        """Parse a 18 byte packet in the Status format.
        """

        self.validate_packet(data)

        packet_length = data[0]
        packet_type = data[1]
        sub_type = data[2]
        sequence_number = data[3]
        command_type = data[4]
        transceiver_type = data[5]
        firmware_version = data[6]

        return {
            'packet_length': packet_length,
            'packet_type': packet_type,
            'sequence_number': sequence_number,
            'sub_type': sub_type,
            'sub_type_name': self.SUB_TYPES.get(sub_type),
            'command_type': command_type,
            'transceiver_type': transceiver_type,
            'firmware_version': firmware_version,
        }
