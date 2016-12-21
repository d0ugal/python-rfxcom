from unittest import TestCase

from rfxcom.protocol.humidity import Humidity

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class HumidityTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x08\x51\x01\x12\x70\x05'
                              b'\x2D\x00\x89')
        self.parser = Humidity()

    def test_parse_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 8,
            'packet_type': 81,
            'packet_type_name': 'Humidity sensors',
            'sequence_number': 18,
            'packet_subtype': 1,
            'packet_subtype_name': 'LaCrosse TX3',
            'id': '0x7005',
            # 'channel': 2, TBC
            'signal_level': 8,
            'humidity': 45,
            'humidity_status': 'Dry',
            'battery_level': 9
        })

        self.assertEquals(str(self.parser), "<Humidity ID:0x7005>")

    def test_parse_bytes2(self):

        self.data = bytearray(b'\x08\x51\x02\x02\xAE\x01'
                              b'\x62\x03\x59')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 8,
            'packet_type': 81,
            'packet_type_name': 'Humidity sensors',
            'sequence_number': 2,
            'packet_subtype': 2,
            'packet_subtype_name': 'LaCrosse WS2300',
            'id': '0xAE01',
            # 'channel': 1, TBC
            'signal_level': 5,
            'humidity': 98,
            'humidity_status': 'Wet',
            'battery_level': 9
        })

        self.assertEquals(str(self.parser), "<Humidity ID:0xAE01>")

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

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Humidity')
