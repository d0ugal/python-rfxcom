from unittest import TestCase

from rfxcom.protocol.rain import Rain

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class RainTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0B\x55\x01\x11\x70\x02\x00\xA7'
                              b'\x2D\x00\x00\x89')
        self.parser = Rain()

    def test_parse_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 11,
            'packet_type': 85,
            'packet_type_name': 'Rain sensors',
            'sequence_number': 17,
            'packet_subtype': 1,
            'packet_subtype_name': 'RGR126/682/918',
            'id': '0x7002',
            # 'channel': 2, TBC
            'signal_level': 8,
            'rain_rate': 167,
            'rain_total': 18432.0,
            'battery_level': 9
        })

        self.assertEquals(str(self.parser), "<Rain ID:0x7002>")

    def test_parse_bytes_subtype2(self):

        self.data = bytearray(b'\x0B\x55\x02\x05\x70\x03\x00\x67'
                              b'\x1A\x01\x02\x45')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 11,
            'packet_type': 85,
            'packet_type_name': 'Rain sensors',
            'sequence_number': 5,
            'packet_subtype': 2,
            'packet_subtype_name': 'PCR800',
            'id': '0x7003',
            # 'channel': 1, TBC
            'signal_level': 4,
            'rain_rate': 1.03,
            'rain_total': 10675.4,
            'battery_level': 5
        })

        self.assertEquals(str(self.parser), "<Rain ID:0x7003>")

    def test_parse_bytes_subtype6(self):

        self.data = bytearray(b'\x0B\x55\x06\x05\x70\x03\x00\x67'
                              b'\x1A\x01\x02\x45')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 11,
            'packet_type': 85,
            'packet_type_name': 'Rain sensors',
            'sequence_number': 5,
            'packet_subtype': 6,
            'packet_subtype_name': 'La Crosse TX5',
            'id': '0x7003',
            # 'channel': 1, TBC
            'battery_level': 5,
            'signal_level': 4
        })

        self.assertEquals(str(self.parser), "<Rain ID:0x7003>")

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

        self.data[2] = 0xEE

        self.assertFalse(self.parser.can_handle(self.data))

        with self.assertRaises(UnknownPacketSubtype):
            self.parser.validate_packet(self.data)

    def test_log_name(self):

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Rain')
