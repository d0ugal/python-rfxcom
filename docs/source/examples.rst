Examples
========


.. code-block:: python

    from asyncio import get_event_loop

    from rfxcom.transport import AsyncioTransport

    loop = get_event_loop()

    # The port name will vary based on the device and operating system used. This
    # was copied from my local machine.
    dev_name = '/dev/serial/by-id/usb-RFXCOM_RFXtrx433_A1WYT9NA-if00-port0'


    def handler(packet):
        """Create a basic packet handler

        This is a very simple handler that will catch all of the packets recieved
        by the RFXCom. The passed in Packet variable will be
        rfxcom.protocol.base.Packet or a subclass if a specific device is detected
        for that packet.
        """

        # Print out the packet - the string representation will show us the type.
        print(packet)

        # Each packet will have a dictionary which contains parsed data.
        print(packet.data)

        # You can access the raw bytes from the packet too.
        print(packet.raw)


    try:
        rfxcom = AsyncioTransport(dev_name, loop, callback=handler)
        loop.run_forever()
    finally:
        loop.close()

This second example shows how you can use different callback handlers for
different packet types.


.. code-block:: python

    from asyncio import get_event_loop

    from rfxcom.transport import AsyncioTransport
    from rfxcom import protocol

    loop = get_event_loop()

    # The port name will vary based on the device and operating system used. This
    # was copied from my local machine.
    dev_name = '/dev/serial/by-id/usb-RFXCOM_RFXtrx433_A1WYT9NA-if00-port0'


    # This is similar to the code in example_1.py but rather than having one
    # handler method which catches all packets we can specify a number of handlers
    # for the different packets we are interested in.
    def status_handler(packet):
        # ignore.
        return


    def elec_handler(packet):
        print("Watts:", packet.data['current_watts'])


    def temp_humidity_handler(packet):
        print("Temp :", packet.data['temperature'])


    def default_callback(bytes_):
        print("???? :\n", list(bytes_), repr(bytes_), '\n')

    try:
        # To provide multiple callbacks we need to pass in a callbacks dict, the
        # key of the dictionary is the Packet handler and then the value is the
        # method to call if that packet type is found.
        # Finally a special value of '*' is used for a fallback handler which will
        # be used to catch any remaining packets.

        rfxcom = AsyncioTransport(dev_name, loop, callbacks={
            protocol.Status: status_handler,
            protocol.Elec: elec_handler,
            protocol.TempHumidity: temp_humidity_handler,
            '*': default_callback,
        })
        loop.run_forever()
    finally:
        loop.close()
