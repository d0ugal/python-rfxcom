from rfxcom.protocol.base import BasePacketHandler


class TempHumidity(BasePacketHandler):

    def __init__(self):

        super(TempHumidity, self).__init__()

        self.PACKET_TYPES = {
            0x52: "Interface message"
        }

        self.SUB_TYPES = {
            0x01: " THGN122/123, THGN132, THGR122/228/238/268",
            0x02: "",
            0x03: "",
            0x04: "",
            0x05: "",
            0x06: "",
            0x07: "",
            0x08: "",
            0x09: "",
            0x0A: "",
            0x0B: "",
        }

    def parse(self, data):
        """Parse a 10 byte packet in the Temperature and humidity sensors.
        """

        self.validate_packet(data)

        packet_length = data[0]
        packet_type = data[1]
        sub_type = data[2]
        sequence_number = data[3]
        id_ = self.dump_hex(data[4:6])

        temperature = ((data[6] & 0x7f) * 256 + data[7]) / 10.0
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
