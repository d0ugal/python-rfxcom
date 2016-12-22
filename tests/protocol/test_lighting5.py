from unittest import TestCase

from rfxcom.protocol.lighting5 import Lighting5

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class Lighting5TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0A\x14\x00\xAD\xF3\x94\xAB'
                              b'\x01\x01\x00\x60')
        self.parser = Lighting5()

    def test_parse_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': "0xF394AB",
            'packet_length': 10,
            'packet_type': 20,
            'packet_type_name': "Lighting5 sensors",
            'packet_subtype': 0,
            'packet_subtype_name': "LightwaveRF, Siemens",
            'sequence_number': 173,
            'unit_code': 1,
            'command': 1,
            'command_text': "On",
            'level': 0,
            'signal_level': 6
        })

        self.assertEquals(str(self.parser), "<Lighting5 ID:0xF394AB>")

    def test_validate_bytes_short(self):

        data = self.data[:1]

        with self.assertRaises(InvalidPacketLength):
            self.parser.validate_packet(data)

    def test_validate_unkown_packet_type(self):

        self.data[1] = 0xFF

        self.assertFalse(self.parser.can_handle(self.data))

        with self.assertRaises(UnknownPacketType):
            self.parser.validate_packet(self.data)

    def test_validate_unknown_sub_type(self):

        self.data[2] = 0xFF

        self.assertFalse(self.parser.can_handle(self.data))

        with self.assertRaises(UnknownPacketSubtype):
            self.parser.validate_packet(self.data)

    def test_log_namer(self):

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Lighting5')
