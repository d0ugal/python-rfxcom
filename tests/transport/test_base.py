from unittest import TestCase
from unittest.mock import Mock, ANY

from serial import Serial

from rfxcom.exceptions import PacketHandlerNotFound, RFXComException
from rfxcom.protocol import Elec
from rfxcom.transport.base import BaseTransport


def _callback(*args, **kwargs):
    pass


def _callback2(*args, **kwargs):
    pass


class BaseTestCase(TestCase):

    def setUp(self):

        self.elec_packet = (b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                            b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')

        self.device = Mock(spec=Serial)

        self.transport = BaseTransport(device=self.device, callback=_callback)
        self.bytes_array = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00')

    def test_format_packet(self):

        bytes_array = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00')
        formatted = self.transport.format_packet(bytes_array)
        expected = '0x11 0x5a 0x01 0x00 0x2e 0xb2 0x03 0x00 0x00'

        self.assertEquals(formatted, expected)

    def test_setup_callbacks_single(self):

        self.assertEquals(self.transport.default_callback, _callback)

        self.assertEquals(
            self.transport.get_callback_parser(self.bytes_array),
            (_callback, ANY)
        )

    def test_setup_callbacks_mutli(self):

        # Setup - handler for Elec and fallback for the rest.
        parser = BaseTransport(device=self.device, callbacks={
            Elec: _callback2,
            '*': _callback,

        })

        # Verify default fallback and callbacks dict contains Elec only.
        self.assertEquals(parser.default_callback, _callback)
        self.assertEquals(parser.callbacks, {
            Elec: _callback2
        })

    def test_get_callback_parser(self):

        # Setup - handler for Elec and fallback for the rest.
        parser = BaseTransport(device=self.device, callbacks={
            Elec: _callback2,
            '*': _callback,

        })

        # create a valid elec packet to call with.
        elec_packet = bytearray(self.elec_packet)

        self.assertEquals(
            parser.get_callback_parser(elec_packet),
            (_callback2, ANY)
        )

    def test_no_packet_handler_found(self):

        # Setup - handler for Elec and fallback for the rest.
        parser = BaseTransport(device=self.device, callbacks={
            Elec: _callback2,
        })

        with self.assertRaises(PacketHandlerNotFound):
            parser.get_callback_parser(self.bytes_array)

    def test_no_callbacks(self):

        with self.assertRaises(RFXComException):
            BaseTransport(device=self.device)

    def test_do_callback(self):

        callback_mock = Mock()

        # Setup - handler for Elec and fallback for the rest.
        parser = BaseTransport(device=self.device, callbacks={
            Elec: callback_mock,
            '*': _callback,

        })

        # create a valid elec packet to call with.
        elec_packet = bytearray(self.elec_packet)

        parser.do_callback(elec_packet)

        callback_mock.assert_called_once()

    def test_log(self):

        self.transport.log.debug("test")
        self.assertEquals(self.transport.log.name,
                          'rfxcom.transport.BaseTransport')

    def test_write(self):

        self.transport.write(self.elec_packet)

        self.device.write.assert_called_once_with(bytearray(self.elec_packet))

    def test_reader(self):

        self.device.read.return_value = self.elec_packet

        self.transport.read()

    def test_read_blank(self):

        self.device.read.return_value = b'\x00'

        self.transport.read()
