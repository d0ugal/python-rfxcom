from argparse import ArgumentParser
from asyncio import get_event_loop
from functools import partial
from logging.config import dictConfig
from sys import stdout

from rfxcom import protocol
from rfxcom.transport import AsyncioTransport

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)-8s %(name)-35s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': stdout,
            'formatter': 'standard'
        }
    },
    'loggers': {
        'rfxcom': {
            'handlers': ['console', ],
            'propagate': True,
            'level': 'DEBUG',
        }
    },
}

def noop(*args, **kwargs):
    pass

def handler(packet):
    print(packet)

def write(rfxcom):
    rfxcom.write(b'\x0D\x00\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')

def main():

    dictConfig(LOGGING)

    loop = get_event_loop()

    parser = ArgumentParser()
    parser.add_argument('device')
    args = parser.parse_args()

    try:
        rfxcom = AsyncioTransport(args.device, loop, callbacks={
            protocol.Status: noop,
            protocol.Elec: noop,
            protocol.TempHumidity: noop,
            '*': handler,
        })
        loop.call_later(2, partial(write, rfxcom))
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
