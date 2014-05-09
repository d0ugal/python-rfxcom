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
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': '/tmp/rfxcom.log',
            'maxBytes': 10 * 1024 * 1024,
        },
    },
    'loggers': {
        'rfxcom': {
            'handlers': ['console', 'file', ],
            'propagate': True,
            'level': 'DEBUG',
        }
    },
}


def status_handler(packet):
    return


def elec_handler(packet):
    print(packet)


def temp_humidity_handler(packet):
    return


def default_callback(packet):
    print("???? :", packet)


def write(rfxcom):
    return


def main():

    dictConfig(LOGGING)

    loop = get_event_loop()

    parser = ArgumentParser()
    parser.add_argument('device')
    args = parser.parse_args()

    try:
        rfxcom = AsyncioTransport(args.device, loop, callbacks={
            protocol.Status: status_handler,
            protocol.Elec: elec_handler,
            protocol.TempHumidity: temp_humidity_handler,
            '*': default_callback,
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
