from serial import Serial

from rfxcom.transport.base import BaseTransport
from rfxcom.protocol import RESET_PACKET, STATUS_PACKET


class AsyncioTransport(BaseTransport):

    def __init__(self, device, loop, callback=None, callbacks=None,
                 SerialClass=None):

        super().__init__(device, callback=callback, callbacks=callbacks)

        if SerialClass is None:
            SerialClass = Serial

        self.loop = loop

        self.dev = SerialClass(device, 38400, timeout=1)

        loop.add_writer(self.dev.fd, self.setup)

    def setup(self):
        """ Perform setup tasks

        - Send a reset to the rfxtrx
        - Attach a reader to the eventloop
        - Send a status packet to the rfxtrx (No earlier than 0.05 seconds
          after the reset packet and no later than 10 seconds after)
        """
        self.loop.remove_writer(self.dev.fd)

        self.dev.flushInput()
        self.write(RESET_PACKET)

        self.loop.add_reader(self.dev.fd, self.reader)

        self.loop.call_later(0.5, self.write, STATUS_PACKET)

    def write(self, data):

        assert type(data) == bytes

        pkt = bytearray(data)
        self.log.info("WRITE: %s" % self.format_packet(pkt))
        self.dev.write(pkt)

    def reader(self):

        data = self.dev.read()

        while True:
            if len(data) > 0:
                if data == b'\x00':
                    return
                pkt = bytearray(data)
                data = self.dev.read(pkt[0])
                pkt.extend(bytearray(data))
                break

        self.log.info("READ : %s" % self.format_packet(pkt))
        self.do_callback(pkt)

    def do_callback(self, pkt):
        callback, parser = self.get_callback_parser(pkt)
        self.loop.call_soon(callback, parser)
