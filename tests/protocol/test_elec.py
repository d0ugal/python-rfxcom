from unittest import TestCase

from rfxcom.protocol.elec import Elec

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class Elec2TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                              b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')
        self.parser = Elec()

    def test_parse_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'count': 3,
            'current_watts': 692,
            'id': "0x2EB2",
            'packet_length': 17,
            'packet_type': 90,
            'sequence_number': 0,
            'sub_type': 1,
            'sub_type_name': "CM119/160",
            'total_watts': 920825.1947099693,
        })

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

    def test_bytes_to_uint_32(self):

        data = self.data[7:11]

        self.assertEqual(self.parser._bytes_to_uint_32(data), 692)

    def test_bytes_to_uint_48(self):

        data = self.data[11:16]

        self.assertEquals(self.parser._bytes_to_uint_48(data), 205957288)

    def test_log_namer(self):

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Elec')
