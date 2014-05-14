from unittest import TestCase

from rfxcom.protocol.status import Status

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class StatusTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0D\x01\x00\x01\x02\x53\x45\x00\x0C'
                              b'\x2F\x01\x01\x00\x00')
        self.parser = Status()

    def test_parse_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result.pop('disabled_protocols'), [
            'AD LightwaveRF',
            'AE Blyss',
            'ATI',
            'BlindsT0',
            'BlindsT1/T2/T3/T4',
            'Byron SX',
            'Display undecoded',
            'FS20',
            'FineOffset/Viking',
            'Lighting4',
            'Meiantech',
            'Mertik',
            'ProGuard',
            'RFU6',
            'RSL',
            'Rubicson',
            'Visonic',
        ])

        self.assertEquals(result.pop('enabled_protocols'), [
            'AC',
            'ARC',
            'Hideki/UPM',
            'HomeEasy EU',
            'La Crosse',
            'Oregon Scientific',
            'X10',
        ])

        self.assertEquals(result, {
            'packet_length': 13,
            'packet_type': 1,
            'sequence_number': 1,
            'sub_type': 0,
            'sub_type_name': 'Response on a mode command',
            'transceiver_type': 83,
            'transceiver_type_text': '433.92MHz transceiver',
            'firmware_version': 69,
            'command_type': 2,
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

        self.data[2] = 0xEE

        self.assertFalse(self.parser.can_handle(self.data))

        with self.assertRaises(UnknownPacketSubtype):
            self.parser.validate_packet(self.data)

    def test_log_namer(self):

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Status')
