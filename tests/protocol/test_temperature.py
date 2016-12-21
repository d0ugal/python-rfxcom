from unittest import TestCase

from rfxcom.protocol.temperature import Temperature

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class TemperatureTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x08\x50\x02\x11\x70\x02\x00\xA7\x89')
        self.parser = Temperature()

    def test_parse_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 8,
            'packet_type': 80,
            'packet_type_name': 'Temperature sensors',
            'sequence_number': 17,
            'packet_subtype': 2,
            'packet_subtype_name': 'THC238/268,THN132,THWR288,THRN122,THN122,AW129/131',
            'temperature': 16.7,
            'id': '0x7002',
            # 'channel': 2, TBC
            'signal_level': 8,
            'battery_level': 9
        })

        self.assertEquals(str(self.parser), "<Temperature ID:0x7002>")

    def test_parse_bytes2(self):

        self.data = bytearray(b'\x08\x50\x03\x02\xAE\x01\x00\x63\x59')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 8,
            'packet_type': 80,
            'packet_type_name': 'Temperature sensors',
            'sequence_number': 2,
            'packet_subtype': 3,
            'packet_subtype_name': 'THWR800',
            'temperature': 9.9,
            'id': '0xAE01',
            # 'channel': 1, TBC
            'signal_level': 5,
            'battery_level': 9
        })
        
        self.assertEquals(str(self.parser), "<Temperature ID:0xAE01>")

    def test_parse_bytes_negative_temp(self):

        self.data = bytearray(b'\x08\x50\x06\x02\xAE\x01\x80\x55\x59')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 8,
            'packet_type': 80,
            'packet_type_name': 'Temperature sensors',
            'sequence_number': 2,
            'packet_subtype': 6,
            'packet_subtype_name': 'TS15C',
            'temperature': -8.5,
            'id': '0xAE01',
            # 'channel': 1, TBC
            'signal_level': 5,
            'battery_level': 9
        })
        
        self.assertEquals(str(self.parser), "<Temperature ID:0xAE01>")

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

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Temperature')
