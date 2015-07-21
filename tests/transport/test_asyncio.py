"""Unit tests for rfxcom.asyncio.AsyncioTransport."""
from unittest import TestCase, mock

from rfxcom.transport import AsyncioTransport

# It's a unittest, let's be flexible
# pylint: disable=C0111,W0212,R0201


def execute_coroutine(coroutine):
    """Execute a coroutine.

    The coroutine is a generator which 'yields from' other iterables in the
    form of asyncio.Future instances. For each generated value, wait for it to
    be done and move on to the next one, until the generator has completed.

    Since there is no loop instance to enter, it might be needed to mock each
    yielded value before executing the coroutine, to avoid blocking situations.

    Exemple:
        with mock.patch('coro.yielded.metod.Function'):
            result = execute_coroutine(coro)

    Althogh this helper is thought to work with coroutined generators, it
    should work with any iterator.

    @param coroutine: an iterable, e.g. an asyncio.coroutine decorated method
      yielding something.

    @returns the return value of the coroutine, or None if nothing is returned
    """
    try:
        future = next(coroutine)
        while not future.done():
            pass
    except StopIteration as exc:
        if hasattr(exc, 'value'):
            return exc.value


class AsyncioTransportTestCase(TestCase):

    """AsyncioTransport test case."""

    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_constructor(self, device, loop):
        unit = AsyncioTransport(device, loop, callback=mock.Mock())
        loop.add_writer.assert_called_once_with(device.fd, unit.setup)

    @mock.patch('rfxcom.transport.asyncio.AsyncioTransport._setup')
    @mock.patch('asyncio.async')
    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_setup(self, device, loop, async, _setup):
        unit = AsyncioTransport(device, loop, callback=mock.Mock())
        # reset mocks which have been 'called' by the constructor
        device.reset_mock()
        loop.reset_mock()
        unit.setup()

        loop.remove_writer.assert_called_once_with(device.fd)
        async.assert_called_once_with(_setup())

    @mock.patch('rfxcom.transport.asyncio.AsyncioTransport.sendRESET')
    @mock.patch('rfxcom.transport.asyncio.AsyncioTransport.sendSTATUS')
    @mock.patch('rfxcom.transport.asyncio.AsyncioTransport.sendMODE')
    @mock.patch('asyncio.sleep')
    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport__setup(self, device, loop, sleep, mode, status, reset):
        unit = AsyncioTransport(device, loop, callback=mock.Mock())
        # reset mocks which have been 'called' by the constructor
        device.reset_mock()
        loop.reset_mock()

        # run: exaust the coroutine generator
        execute_coroutine(unit._setup())

        loop.add_reader.assert_called_with(device.fd, unit.read)
        reset.assert_called_once_with()
        sleep.assert_has_calls((mock.ANY, mock.ANY))
        slept_time = sleep.call_args[0][0]
        # by spec it needs to be between 0.5ms and 9000ms
        self.assertGreater(slept_time, 0.05)
        self.assertLess(slept_time, 9)
        mode.assert_called_once_with()
        status.assert_called_once_with()
        loop.call_soon.assert_called_once_with(loop.add_writer, device.fd,
                                               unit._writer)

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

    @mock.patch('rfxcom.transport.asyncio.AsyncioTransport.do_callback')
    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_read(self, device, loop, callback):

        unit = AsyncioTransport(device, loop, callback=mock.Mock())

        def fake_read(*x):
            data = {
                (): b'\x02',
                (2, ): b'\x01\x01'
            }
            return data[x]
        device.read.side_effect = fake_read

        expected_result = b'\x02\x01\x01'
        self.assertEquals(unit.read(), expected_result)
        callback.assert_called_once_with(expected_result)

    @mock.patch(
        'rfxcom.transport.asyncio.AsyncioTransport.get_callback_parser')
    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_do_callback(self, device, loop, get_parser):

        cb = mock.Mock()
        get_parser.return_value = (cb, "test")

        unit = AsyncioTransport(device, loop, callback=mock.Mock())

        def fake_read(*x):
            data = {
                (): b'\x02',
                (2, ): b'\x01\x01'
            }
            return data[x]
        device.read.side_effect = fake_read

        expected_result = b'\x02\x01\x01'
        self.assertEquals(unit.read(), expected_result)
        loop.call_soon_threadsafe.assert_called_once_with(
            AsyncioTransport._do_async_callback, cb, "test")

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

    @mock.patch('asyncio.AbstractEventLoop')
    @mock.patch('serial.Serial')
    def test_transport_doesnt_write_with_emtpy_queue(self, device, loop):
        unit = AsyncioTransport(device, loop, callback=mock.Mock())

        # Call write and verify it was added to the queue
        unit.write_queue = []
        unit._writer()

        self.assertFalse(device.write.called)
