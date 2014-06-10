from unittest import TestCase, mock

from rfxcom.transport import AsyncioTransport
from rfxcom.protocol import RESET_PACKET, MODE_PACKET, STATUS_PACKET


class AsyncioTransportTestCase(TestCase):

    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_constructor(self, device, loop):
        unit = AsyncioTransport(device, loop, callback=mock.Mock())
        loop.add_writer.assert_called_once_with(device.fd, unit.setup)

    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    @mock.patch('rfxcom.transport.AsyncioTransport.write')
    def test_transport_setup(self, unit_write, device, loop):

        unit = AsyncioTransport(device, loop, callback=mock.Mock())
        unit.setup()

        loop.remove_writer.assert_called_with(device.fd)
        device.write.assert_called_once(RESET_PACKET)
        loop.call_later.assert_any_call(mock.ANY,
                                        super(AsyncioTransport, unit).write,
                                        STATUS_PACKET)
        unit_write.assert_called_once_with(MODE_PACKET)
