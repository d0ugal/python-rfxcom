from asyncio import get_event_loop
from unittest import TestCase, mock

from rfxcom.transport import AsyncioTransport

from rfxcom.protocol import RESET_PACKET, STATUS_PACKET


class AsyncioTransportTestCase(TestCase):

    def test_loop_once(self):

        loop = get_event_loop()

        def handler(*args, **kwargs):
            pass

        device = mock.MagicMock()

        AsyncioTransport(device, loop, callback=handler)
        loop._run_once()

        device.write.assert_has_call(bytearray(RESET_PACKET))
        device.write.assert_has_call(bytearray(STATUS_PACKET))
