from datetime import datetime

from rfxcom.exceptions import PacketHandlerNotFound
from rfxcom.protocol import HANDLERS


def n():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")


class BaseTransport:

    def __init__(self, device, callback=None, callbacks=None):

        self.device = device

        self._setup_callbacks(callback, callbacks)

    def format_packet(self, pkt):
        h = " ".join("0x{0:02x}".format(x) for x in pkt)
        return "%s" % (h)

    def log(self, message):
        print(n(), message)

    def _setup_callbacks(self, callback, callbacks):

        if callback is None and callbacks is None:
            raise Exception("bleh")
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

    def do_callback(self, pkt):

        callback, parser = self.get_callback_parser(pkt)

        callback(parser)
