"""
rfxcom.transport.asyncio
========================

"""

import asyncio

from rfxcom.transport.base import BaseTransport
from rfxcom.protocol import RESET_PACKET, STATUS_PACKET, MODE_PACKET


class AsyncioTransport(BaseTransport):
    def __init__(self, device, loop, callback=None, callbacks=None,
                 SerialClass=None):

        super().__init__(device, callback=callback, callbacks=callbacks,
                         SerialClass=SerialClass)

        self.loop = loop
        asyncio.async(self._setup())

    def _setup(self):
        """Performs the RFXtrx initialisation protocol in a Future.

        Currently this is the rough workflow of the interactions with the
        RFXtrx. We also do a few extra things - flush the buffer, and attach
        readers/writers to the asyncio loop.

        1. Write a RESET packet (write all zeros)
        2. Wait at least 50ms and less than 9000ms
        3. Write the STATUS packet to verify the device is up.
        4. Receive status response
        5. Write the MODE packet to enable or disabled the required protocols.
        """
        self.log.info("Adding reader to prepare to receive.")
        self.loop.add_reader(self.dev.fd, self.read)

        self.log.info("Flushing the RFXtrx buffer.")
        self.flushSerialInput()

        self.log.info("Writing the reset packet to the RFXtrx. (blocking)")
        yield from self.sendRESET()

        self.log.info("Wating 0.4s")
        yield from asyncio.sleep(0.4)

        self.log.info("Write the status packet (blocking)")
        yield from self.sendSTATUS()

        # TODO receive status response, compare it with the needed MODE and
        # request a new MODE if required. Currently MODE is always sent.

        self.log.info("Adding mode packet to the write queue (blocking)")
        yield from self.sendMODE()

    @asyncio.coroutine
    def flushSerialInput(self):
        self.dev.flushInput()

    @asyncio.coroutine
    def sendRESET(self):
        super().write(RESET_PACKET)

    @asyncio.coroutine
    def sendMODE(self):
        super().write(MODE_PACKET)

    @asyncio.coroutine
    def sendSTATUS(self):
        super().write(STATUS_PACKET)

    def do_callback(self, pkt):
        """Add the callback to the event loop, we use call soon because we just
        want it to be called at some point, but don't care when particularly.
        """
        callback, parser = self.get_callback_parser(pkt)

        if asyncio.iscoroutinefunction(callback):
            self.loop.call_soon_threadsafe(self._do_async_callback,
                                           callback, parser)
        else:
            self.loop.call_soon(callback, parser)

    @staticmethod
    def _do_async_callback(callback, parser):
        """ Call a the callback coroutine function in the event loop
        :param callback: Coroutine function
        :param parser: Packet parser found for received packet
        """
        asyncio.async(callback(parser))

    def read(self):
        """We have been called to read! As a consumer, continue to read for
        the length of the packet and then pass to the callback.
        """

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
        return pkt
