from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketType,
                               UnknownPacketSubtype, RFXComException)


class BasePacket:
    """
    The base class for all packet handling classes. Provides a number of simple
    helper methods and outlines the API.
    """

    def __init__(self):

        self.PACKET_TYPES = {}
        self.SUB_TYPES = {}

    def dump_hex(self, data):
        """Given some bytes return the hex representation."""
        return "0x%s" % (''.join('{:02x}'.format(x) for x in data)).upper()

    def parse(self, data):
        """Stub method to be implemented by subclasses. The parse method
        should accept a bytearray, parse it and return a dictionary containing
        the parsed values.
        """
        raise NotImplementedError()

    def load(self, data):
        """This is the entrance method for all data which is used to store the
        raw data and start parsing the data.

        :param data: The raw untouched bytearray as recieved by the RFXtrx
        :type data: bytearray

        :return: The parsed data represented in a dictionary
        :rtype: dict
        """
        self.raw = data
        self.data = self.parse(data)
        return self.data


class BasePacketHandler(BasePacket):

    def can_handle(self, data):

        try:
            return self.validate_packet(data)
        except RFXComException:
            return False

    def validate_packet(self, data):
        """Validate a packet.

        Validate against the following checks, raising exceptions if they fail
        and return True when they all pass.
        """

        # Validate length.
        # The first byte in the packet should be equal to the number of
        # remaining bytes (i.e. length excluding the first byte).
        expected_length = data[0] + 1

        if len(data) != expected_length:
            raise InvalidPacketLength(
                "Expected packet length to be %s bytes but it was %s bytes"
                % (expected_length, len(data))
            )

        # Validate Packet Type.
        # This specifies the family of devices. Check its one of the supported
        # Elec2 packet types
        packet_type = data[1]

        if self.PACKET_TYPES and packet_type not in self.PACKET_TYPES:
            types = ",".join("0x{:02x}".format(pt) for pt in self.PACKET_TYPES)
            raise UnknownPacketType(
                "Expected packet type to be one of [%s] but recieved %s"
                % (types, packet_type)
            )

        # Validate Sub Type.
        # The first byte in the packet should be equal to the number of
        # remaining bytes (i.e. length excluding the first byte).
        sub_type = data[2]

        if self.SUB_TYPES and sub_type not in self.SUB_TYPES:
            types = ",".join("0x{:02x}".format(pt) for pt in self.SUB_TYPES)
            raise UnknownPacketSubtype(
                "Expected packet type to be one of [%s] but recieved %s"
                % (types, sub_type))

        return True


class Packet(BasePacketHandler):

    def can_handle(self, data):
        return True

    def validate_packet(self, data):
        return True

    def parse(self, data):

        packet_length = data[0]
        packet_type = data[1]
        sub_type = data[2]

        return {
            'packet_length': packet_length,
            'packet_type': packet_type,
            'sub_type': sub_type,
            'sub_type_name': self.SUB_TYPES.get(sub_type),
            'packet': data,
        }
