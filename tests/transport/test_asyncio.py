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

    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_read_nothing(self, device, loop):

        device.read.return_value = b''

        unit = AsyncioTransport(device, loop, callback=mock.Mock())

        with mock.patch.object(unit, 'log') as unit_log:
            unit.read()
            unit_log.warning.assert_called_once_with(
                "READ : Nothing received")

    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_read_empty_patcket(self, device, loop):

        device.read.return_value = b'\x00'

        unit = AsyncioTransport(device, loop, callback=mock.Mock())

        with mock.patch.object(unit, 'log') as unit_log:
            unit.read()
            unit_log.warning.assert_called_once_with(
                "READ : Empty packet (Got \\x00)")

    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_read(self, device, loop):

        unit = AsyncioTransport(device, loop, callback=mock.Mock())

        call_map = {
            (): b'\x02',
            (2, ): b'\x01\x01'
        }

        device.read = lambda *x: call_map[x]

        self.assertEquals(unit.read(), b'\x02\x01\x01')

    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_write_from_queue(self, device, loop):

        payload = b'\x01\x01'
        unit = AsyncioTransport(device, loop, callback=mock.Mock())

        # Call write and verify it was added to the queue
        unit.write(payload)
        self.assertIn(payload, unit.write_queue)

        unit._writer()

        device.write.assert_called_once_with(payload)
