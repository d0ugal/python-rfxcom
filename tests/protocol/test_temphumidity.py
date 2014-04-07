from unittest import TestCase

from rfxcom.protocol.temphumidity import TempHumidity

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class TempHumidityTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0A\x52\x02\x11\x70\x02\x00\xA7'
                              b'\x2D\x00\x89')
        self.parser = TempHumidity()

    def test_parse_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEqual(result, {
            'packet_length': 10,
            'packet_type': 82,
            'sequence_number': 17,
            'sub_type': 2,
            'sub_type_name': '',
            'temperature': 16.7,
            'id': '0x7002',
            'signal_strength': 137,
            'humidity': 45,
            'humidity_status': 0,
            'battery_signal_level': 137,
        })

    def test_negative_temp(self):

        self.data = bytearray(b'\x0A\x52\x02\x11\x70\x02\x80\xA7'
                              b'\x2D\x00\x89')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEqual(result['temperature'], -16.7)

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

        self.assertEqual(self.parser.log.name, 'rfxcom.protocol.TempHumidity')
