from unittest import TestCase

from rfxcom.protocol.lighting2 import Lighting2

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class Lighting2TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0B\x11\x00\x01\x01\x11\xF3\x42'
                              b'\x0A\x01\x0F\x40')
        self.parser = Lighting2()

    def test_parse_frame_chacon_54781_on(self):

        self.data = bytearray(b'\x0B\x11\x00\x01\x01\x11\xF3\x42'
                              b'\x0A\x01\x0F\x40')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': "0x0111F342",
            'packet_length': 11,
            'packet_type': 17,
            'packet_type_name': "Lighting2 sensors",
            'packet_subtype': 0,
            'packet_subtype_name': "AC",
            'sequence_number': 1,
            'unit_code': 10,
            'command': 1,
            'command_text': "On",
            'dim_level': 100,
            'signal_level': 4
        })

        self.assertEquals(str(self.parser), "<Lighting2 ID:0x0111F342>")

    def test_parse_frame_chacon_54781_off(self):

        self.data = bytearray(b'\x0B\x11\x00\x03\x01\x11\xF3\x42'
                              b'\x0A\x00\x00\x50')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': "0x0111F342",
            'packet_length': 11,
            'packet_type': 17,
            'packet_type_name': "Lighting2 sensors",
            'packet_subtype': 0,
            'packet_subtype_name': "AC",
            'sequence_number': 3,
            'unit_code': 10,
            'command': 0,
            'command_text': "Off",
            'dim_level': 0,
            'signal_level': 5,
        })

        self.assertEquals(str(self.parser), "<Lighting2 ID:0x0111F342>")

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

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Lighting2')
