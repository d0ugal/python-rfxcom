from unittest import TestCase
from unittest.mock import Mock, ANY

from rfxcom.exceptions import PacketHandlerNotFound
from rfxcom.protocol import Elec
from rfxcom.transport.base import BaseTransport


def _dummy_callback(*args, **kwargs):
    pass


def _dummy_callback2(*args, **kwargs):
    pass


class BaseTestCase(TestCase):

    def setUp(self):

        self.parser = BaseTransport(device=None, callback=_dummy_callback)
        self.bytes_array = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00')

    def test_format_packet(self):

        bytes_array = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00')
        formatted = self.parser.format_packet(bytes_array)
        expected = '0x11 0x5a 0x01 0x00 0x2e 0xb2 0x03 0x00 0x00'

        self.assertEquals(formatted, expected)

    def test_setup_callbacks_single(self):

        self.assertEquals(self.parser.default_callback, _dummy_callback)

        self.assertEquals(
            self.parser.get_callback_parser(self.bytes_array),
            (_dummy_callback, ANY)
        )

    def test_setup_callbacks_mutli(self):

        # Setup - handler for Elec and fallback for the rest.
        parser = BaseTransport(device=None, callbacks={
            Elec: _dummy_callback2,
            '*': _dummy_callback,

        })

        # Verify default fallback and callbacks dict contains Elec only.
        self.assertEquals(parser.default_callback, _dummy_callback)
        self.assertEquals(parser.callbacks, {
            Elec: _dummy_callback2
        })

    def test_get_callback_parser(self):

        # Setup - handler for Elec and fallback for the rest.
        parser = BaseTransport(device=None, callbacks={
            Elec: _dummy_callback2,
            '*': _dummy_callback,

        })

        # create a valid elec packet to call with.
        elec_packet = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                                b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')

        self.assertEquals(
            parser.get_callback_parser(elec_packet),
            (_dummy_callback2, ANY)
        )

    def test_no_packet_handler_found(self):

        # Setup - handler for Elec and fallback for the rest.
        parser = BaseTransport(device=None, callbacks={
            Elec: _dummy_callback2,
        })

        with self.assertRaises(PacketHandlerNotFound):
            parser.get_callback_parser(self.bytes_array)

    def test_do_callback(self):

        callback_mock = Mock()

        # Setup - handler for Elec and fallback for the rest.
        parser = BaseTransport(device=None, callbacks={
            Elec: callback_mock,
            '*': _dummy_callback,

        })

        # create a valid elec packet to call with.
        elec_packet = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                                b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')

        parser.do_callback(elec_packet)

        callback_mock.assert_called_once()

    def test_log(self):

        self.parser.log(message="test")
