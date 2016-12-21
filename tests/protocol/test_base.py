from unittest import TestCase

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.exceptions import InvalidPacketLength
from rfxcom.exceptions import MalformedPacket


class BaseTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                              b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')
        self.parser = BasePacketHandler()

    def test_validate_bytes(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))

    def test_validate_bytes_short(self):

        data = self.data[:1]

        with self.assertRaises(InvalidPacketLength):
            self.parser.validate_packet(data)

        self.assertFalse(self.parser.can_handle(data))

    def test_malformed_packet(self):

        data = self.data[0:3]
        data[0] = 2

        with self.assertRaises(MalformedPacket):
            self.parser.validate_packet(data)

    def test_not_implemented(self):

        with self.assertRaises(NotImplementedError):
            self.parser.load(self.data)

    def test_log_namer(self):

        self.assertEquals(self.parser.log.name,
                          'rfxcom.protocol.BasePacketHandler')
