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
    print("Status :\n", packet.data, '\n')


def elec_handler(packet):
    print("Elec   :\n", packet.data, '\n')


def temp_humidity_handler(packet):
    print("Temp   :\n", packet.data, '\n')


def default_callback(bytes_):
    print("????   :\n", list(bytes_), repr(bytes_), '\n')

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
