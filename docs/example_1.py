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
