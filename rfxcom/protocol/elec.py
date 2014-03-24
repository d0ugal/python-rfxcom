from rfxcom.protocol.base import BasePacketHandler


class Elec(BasePacketHandler):

    def __init__(self):

        super().__init__()

        self.PACKET_TYPES = {
            0x5A: "Energy usage sensors"
        }

        self.SUB_TYPES = {
            0x01: "CM119/160",
            0x02: "CM180",
        }

    def bytes_to_uint_32(self, bytes_):
        """Converts an array of 4 bytes to a 32bit integer.
        """
        return ((bytes_[0] * pow(2, 24)) +
                (bytes_[1] << 16) + (bytes_[2] << 8) + bytes_[3])

    def bytes_to_uint_48(self, bytes_):
        """Converts an array of 6 bytes to a 48bit integer.
        """
        return ((bytes_[0] * pow(2, 40)) + (bytes_[1] * pow(2, 32)) +
                (bytes_[2] * pow(2, 24)) + (bytes_[3] << 16) +
                (bytes_[4] << 8) + bytes_[4])

    def parse(self, data):
        """Parse a 18 byte packet in the Elec format.
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
        battery_level = data[16]
        rssi = data[17]

        current_watts = self.bytes_to_uint_32(instant)
        total_watts = self.bytes_to_uint_48(total) / TOTAL_DIVISOR

        return {
            'battery_level': battery_level,
            'count': count,
            'current_watts': current_watts,
            'id': id_,
            'packet_length': packet_length,
            'packet_type': packet_type,
            'sequence_number': sequence_number,
            'signal_strength': rssi,
            'sub_type': sub_type,
            'sub_type_name': self.SUB_TYPES.get(sub_type),
            'total_watts': total_watts,
        }
