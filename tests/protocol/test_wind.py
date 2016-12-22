from unittest import TestCase

from rfxcom.protocol.wind import Wind

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class WindTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x10\x56\x01\x05\x1C\x00\x00\xA2\x00'
                              b'\x02\x01\xB2\x00\x0C\x46\xA8\x98')
        self.parser = Wind()

    def test_parse_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': "0x1C00",
            'packet_length': 16,
            'packet_type': 86,
            'packet_type_name': 'Wind sensors',
            'sequence_number': 5,
            'packet_subtype': 1,
            'packet_subtype_name': "WTGR800",
            'direction': 162,
            'wind_gust': 43.400000000000006,
            'av_speed': 0.2,
            'battery_level': 8,
            'signal_level': 9
        })

        self.assertEquals(str(self.parser), "<Wind ID:0x1C00>")

    def test_parse_bytes_subtype4(self):

        self.data = bytearray(b'\x10\x56\x04\x02\xB2\x06\x00\x0F\x00'
                              b'\x09\x01\x0E\x80\x0F\x02\x09\x56')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': "0xB206",
            'packet_length': 16,
            'packet_type': 86,
            'packet_type_name': 'Wind sensors',
            'sequence_number': 2,
            'packet_subtype': 4,
            'packet_subtype_name': "TFA",
            'direction': 15,
            'wind_gust': 27.0,
            'wind_chill': 52.1,
            'temperature': -1.5,
            'av_speed': 0.9,
            'battery_level': 6,
            'signal_level': 5
        })

        self.assertEquals(str(self.parser), "<Wind ID:0xB206>")

    def test_parse_bytes_subtype5(self):

        self.data = bytearray(b'\x10\x56\x05\x09\x5D\x01\x01\x00\x00'
                              b'\x02\x01\x18\x00\x0C\x46\xA8\x64')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': "0x5D01",
            'packet_length': 16,
            'packet_type': 86,
            'packet_type_name': 'Wind sensors',
            'sequence_number': 9,
            'packet_subtype': 5,
            'packet_subtype_name': "UPM WDS500",
            'direction': 256,
            'wind_gust': 28.0,
            'battery_level': 4,
            'signal_level': 6
        })

        self.assertEquals(str(self.parser), "<Wind ID:0x5D01>")

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

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Wind')
