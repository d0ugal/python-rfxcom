RFXCOM
======

.. image:: http://img.shields.io/travis/d0ugal/python-rfxcom.svg?style=flat
   :alt: Build Status
   :target: https://travis-ci.org/d0ugal/python-rfxcom

.. image:: http://img.shields.io/coveralls/d0ugal/python-rfxcom.svg?style=flat
   :alt: Coverage
   :target: https://coveralls.io/r/d0ugal/python-rfxcom?branch=master

.. image:: http://img.shields.io/pypi/v/rfxcom.svg?style=flat
   :alt: PyPI Version
   :target: https://pypi.python.org/pypi/rfxcom

.. image:: http://img.shields.io/pypi/dm/rfxcom.svg?style=flat
   :alt: PyPI Downloads
   :target: https://pypi.python.org/pypi/rfxcom


A Python library for working with your `RFXTrx`_ for automation projects.

This library is designed to work with Python 3.3+ [#]_ and `asyncio`_ (but
other transports can be implemented). Currently it is primarily used by the
`home`_ project, a dashboard for managing and visualising your home automation
devices.

This library is relatively new and thus the number of devices are limited to
those that @d0ugal owns. This means, that the current list of fully supported
protocols are:

1. `Status Packets`_ from the `RFXTrx`_ itself.
2. `Energy usage sensors`_ (such as the Owl CM119/160 and Owl CM180)
3. `Temperature and humidity sensors`_ (such as the Oregon THGN132)
4. `Lighting and power control`_ devices from LightwaveRF

If you want to use a device and you don't think its supported or you are unsure
then please `open an issue`_.


Installation
------------

It is recommended that you get the latest version from PyPI with pip::

    pip install rfxcom

However, if you want to grab the latest development version you can download
the repository directly from github and run ``python setup.py install`` in the
root of the repository.


Documentation
-------------

`View the documentation on Read The Docs`_.


Quick Example
-------------

The following example shows some basic usage of this library, it sets up the
asyncio event loop, points the library to the serial device path and attaches
a simple handler function which prints out information about all the packets it
receives. For example, see what it will `output for energy usage sensors`_.::

    from asyncio import get_event_loop
    from rfxcom.transport import AsyncioTransport

    dev_name = '/dev/serial/by-id/usb-RFXCOM_RFXtrx433_A1WYT9NA-if00-port0'
    loop = get_event_loop()

    def handler(packet):
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


Contributing
------------

If you would like to contribute to python-rfxcom, you will need to use `tox`_
to run the tests. This will test against Python 3.3, Python 3.4, pyflakes for
code linting and build the documentation. To do this, you simply need to
install tox and then call tox from the root of the python-rfxcom git
repository. ::

    pip install tox
    tox

Don't worry if you can't test against Python 3.3 and Python 3.4 locally, many
people will only have one installed. We use the brilliant `Travis CI`_ to
verify all pull requests.

.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _Energy usage sensors: http://rfxcom.readthedocs.org/en/latest/ref/protocol/elec.html
.. _home: https://github.com/d0ugal/home
.. _Lighting and power control: http://rfxcom.readthedocs.org/en/latest/ref/protocol/lighting5.html
.. _open an issue: https://github.com/d0ugal/python-rfxcom/issues/new
.. _output for energy usage sensors: http://rfxcom.readthedocs.org/en/latest/ref/protocol/elec.html
.. _RFXTrx: http://www.rfxcom.com/store/Transceivers/14103
.. _Status Packets: http://rfxcom.readthedocs.org/en/latest/ref/protocol/status.html
.. _Temperature and humidity sensors: http://rfxcom.readthedocs.org/en/latest/ref/protocol/temphumidity.html
.. _tox: https://pypi.python.org/pypi/tox
.. _Travis CI: https://travis-ci.org/d0ugal/python-rfxcom
.. _View the documentation on Read The Docs: http://rfxcom.readthedocs.org/en/latest/

.. [#] However, given enough interest previous versions can be supported:
   https://github.com/d0ugal/python-rfxcom/pull/1
