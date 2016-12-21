from unittest import TestCase

from rfxcom.protocol.ultraviolet import UltraViolet

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class UltraVioletTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x09\x57\x01\x00\x2E\xB2\x03\x05\x00\x69')
        self.parser = UltraViolet()

    def test_parse_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': "0x2EB2",
            'packet_length': 9,
            'packet_type': 87,
            'packet_type_name': 'UV sensors',
            'sequence_number': 0,
            'packet_subtype': 1,
            'packet_subtype_name': "UVN128, UV138",
            'uv': 3,
            'battery_level': 9,
            'signal_level': 6
        })

        self.assertEquals(str(self.parser), "<UltraViolet ID:0x2EB2>")

    def test_parse_bytes_subtype3(self):

        self.data = bytearray(b'\x09\x57\x03\x00\x2E\xB2\x03\x00\x16\x69')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': "0x2EB2",
            'packet_length': 9,
            'packet_type': 87,
            'packet_type_name': 'UV sensors',
            'sequence_number': 0,
            'packet_subtype': 3,
            'packet_subtype_name': "TFA",
            'uv': 3,
            'temperature': 2.2,
            'battery_level': 9,
            'signal_level': 6
        })

        self.assertEquals(str(self.parser), "<UltraViolet ID:0x2EB2>")

    def test_parse_bytes_subtype3_negative_temp(self):

        self.data = bytearray(b'\x09\x57\x03\x00\x2E\xB2\x05\x80\x16\x54')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': "0x2EB2",
            'packet_length': 9,
            'packet_type': 87,
            'packet_type_name': 'UV sensors',
            'sequence_number': 0,
            'packet_subtype': 3,
            'packet_subtype_name': "TFA",
            'uv': 5,
            'temperature': -2.2,
            'battery_level': 4,
            'signal_level': 5
        })

        self.assertEquals(str(self.parser), "<UltraViolet ID:0x2EB2>")
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

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.UltraViolet')
