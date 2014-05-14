"""
rfxcom.transport.asyncio
========================

"""

from rfxcom.transport.base import BaseTransport
from rfxcom.protocol import RESET_PACKET, STATUS_PACKET, MODE_PACKET


class AsyncioTransport(BaseTransport):

    def __init__(self, device, loop, callback=None, callbacks=None,
                 SerialClass=None):

        super().__init__(device, callback=callback, callbacks=callbacks)

        self.loop = loop
        self.write_queue = []

        self.log.info("Attaching writer for setup.")
        loop.add_writer(self.dev.fd, self.setup)

    def setup(self):
        """ Perform setup tasks

        - Send a reset to the rfxtrx
        - Attach a reader to the eventloop
        - Send a status packet to the rfxtrx (No earlier than 0.05 seconds
          after the reset packet and no later than 10 seconds after)

        The setup method is blocking, because the series of events is important
        and we can't do anything until its done anyway. After that it removes
        itself and adds the _writer method which then writes in the event loop
        without blocking.
        """
        self.log.info("Removing setup writer.")
        self.loop.remove_writer(self.dev.fd)

        self.log.info("Flushing the RFXtrx.")
        self.dev.flushInput()

        self.log.info("Writing the reset packet to the RFXtrx. (blocking)")
        super().write(RESET_PACKET)

        self.log.info("Adding reader to prepare to receive.")
        self.loop.add_reader(self.dev.fd, self.read)

        self.log.info("Adding status packet to the write queue.")
        self.write(STATUS_PACKET)

        self.log.info("Adding mode packet to the write queue.")
        self.write(MODE_PACKET)

        self.log.info("Adding the writer in 0.1 seconds.")
        self.loop.call_later(
            0.1, self.loop.add_writer, self.dev.fd, self._writer)

    def _writer(self):
        """We have been called to write! Take the oldest item off the queue
        and use the write method on BaseTransport.
        """
        l = len(self.write_queue)

        if l > 0:
            self.log.debug("Serving from write queue (length %s)" % l)
            super().write(self.write_queue.pop(0))

    def write(self, data):
        """Add a data packet to the write queue. In this case, its a simple
        list. which is then consumed. This method is as light as possible.
        """
        self.write_queue.append(data)

    def do_callback(self, pkt):
        """Add the callback to the event loop, we use call soon because we just
        want it to be called at some point, but don't care when particularly.
        """
        callback, parser = self.get_callback_parser(pkt)
        self.loop.call_soon(callback, parser)

    def read(self):
        """We have been called to read! As a consumer, continue to read for
        the length of the packet and then pass to the callback.
        """

        self.log.debug("Starting read.")

        data = self.dev.read()

        if len(data) == 0:
            self.log.warning("READ : Nothing received")
            return

        if data == b'\x00':
            self.log.warning("READ : Empty packet (Got \\x00)")
            return

        pkt = bytearray(data)
        data = self.dev.read(pkt[0])
        pkt.extend(bytearray(data))

        self.log.info("READ : %s" % self.format_packet(pkt))
        self.do_callback(pkt)

        self.log.debug("Finished read.")
