"""
rfxcom.transport.base
=====================

"""

from logging import getLogger

from serial import Serial

from rfxcom.exceptions import PacketHandlerNotFound, RFXComException
from rfxcom.protocol import HANDLERS


class BaseTransport:

    def __init__(self, device, callback=None, callbacks=None,
                 SerialClass=None):

        self.log = getLogger('rfxcom.transport.%s' % self.__class__.__name__)

        if SerialClass is None:
            SerialClass = Serial

        if isinstance(device, str):
            self.dev = SerialClass(device, 38400, timeout=1)
        else:
            self.dev = device

        self._setup_callbacks(callback, callbacks)

    def format_packet(self, pkt):
        return " ".join("0x{0:02x}".format(x) for x in pkt)

    def _setup_callbacks(self, callback, callbacks):

        if callback is None and callbacks is None:
            raise RFXComException(
                "Either callback or callbacks must be provided.")
        elif callbacks is None:
            self.callbacks = {}
            self.default_callback = callback
        elif callback is None:
            self.callbacks = callbacks
            self.default_callback = self.callbacks.pop('*', None)

    def get_callback_parser(self, pkt):

        for PacketParser, callback in self.callbacks.items():

            parser = PacketParser()

            if parser.can_handle(pkt):
                parser.load(pkt)
                return callback, parser

        if not self.default_callback:
            raise PacketHandlerNotFound("No packet handler found for %s" %
                                        self.format_packet(pkt))

        for PacketParser in HANDLERS:

            parser = PacketParser()
            if parser.can_handle(pkt):
                parser.load(pkt)
                break

        return self.default_callback, parser

    def write(self, data):

        assert type(data) == bytes

        pkt = bytearray(data)
        self.log.info("WRITE: %s" % self.format_packet(pkt))
        self.dev.write(pkt)

    def read(self):

        self.log.debug("READ : STARTING")
        data = self.dev.read()

        while True:

            if len(data) == 0:
                self.log.debug("READ : Nothing received")
                return

            if data == b'\x00':
                self.log.debug("READ : Empty packet (Got \x00)")
                return

            pkt = bytearray(data)
            data = self.dev.read(pkt[0])
            pkt.extend(bytearray(data))
            break

        self.log.info("READ : %s" % self.format_packet(pkt))
        self.do_callback(pkt)

    def do_callback(self, pkt):

        callback, parser = self.get_callback_parser(pkt)

        callback(parser)
