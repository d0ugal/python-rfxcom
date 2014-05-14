Welcome to Python RFXCom's Documentation
========================================

Python RFXCom is a library for easily working with the 433MHz RFXtrx device
from RFXCom via the serial over USB interface. This library is written for
Python 3.3+ and makes use of asyncio for an event based architecture.

For a quick start, see the following example is.

.. code-block:: python

    from asyncio import get_event_loop
    from rfxcom.transport import AsyncioTransport

    loop = get_event_loop()

    dev_name = '/dev/serial/by-id/usb-RFXCOM_RFXtrx433_A1WYT9NA-if00-port0'

    def handler(packet):
        print(packet.data)

    try:
        rfxcom = AsyncioTransport(dev_name, loop, callback=handler)
        loop.run_forever()
    finally:
        loop.close()

Contents:

.. toctree::
   :maxdepth: 2

   examples


API Reference Documentation:

.. toctree::
   :maxdepth: 1

   ref/index
   ref/protocol/index
   ref/transport/index
