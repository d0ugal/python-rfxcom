from rfxcom.transport.base import BaseTransport
from rfxcom.protocol import RESET_PACKET, STATUS_PACKET


class AsyncioTransport(BaseTransport):

    def __init__(self, device, loop, callback=None, callbacks=None,
                 SerialClass=None):

        super().__init__(device, callback=callback, callbacks=callbacks)

        self.loop = loop

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

        self.loop.add_reader(self.dev.fd, self.read)

        self.loop.call_later(0.1, self.write, STATUS_PACKET)

    def do_callback(self, pkt):
        callback, parser = self.get_callback_parser(pkt)
        self.loop.call_soon(callback, parser)
