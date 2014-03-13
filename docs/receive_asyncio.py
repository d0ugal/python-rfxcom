from asyncio import get_event_loop
from datetime import datetime

from serial import Serial


def n():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")


def l(pkt):
    h = " ".join("0x{0:02x}".format(x) for x in pkt)
    return "%s" % (h)


def reader(dev):

    data = dev.read()

    while True:
        if len(data) > 0:
            if data == b'\x00':
                return
            pkt = bytearray(data)
            data = dev.read(pkt[0])
            pkt.extend(bytearray(data))
            break

    print(n(), "READ : %s" % l(pkt))


def write(dev, data):

    assert type(data) == bytes
    pkt = bytearray(data)
    print(n(), "WRITE: %s" % l(pkt))
    dev.write(pkt)


def setup(dev, loop):

    print(n(), "Starting setup.")

    loop.remove_writer(dev.fd)

    dev.flushInput()
    reset = b'\x0D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    write(dev, reset)

    loop.add_reader(dev.fd, reader, dev)

    status = b'\x0D\x00\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    loop.call_later(2, write, dev, status)


dev_name = '/dev/serial/by-id/usb-RFXCOM_RFXtrx433_A1WYT9NA-if00-port0'
dev = Serial(dev_name, 38400, timeout=1)

loop = get_event_loop()

try:
    loop.add_writer(dev.fd, setup, dev, loop)
    loop.run_forever()
finally:
    loop.close()
