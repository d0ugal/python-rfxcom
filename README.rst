RFXCOM
======

.. image:: https://secure.travis-ci.org/d0ugal/rfxcom.png
   :alt: Build Status
   :target: https://travis-ci.org/d0ugal/rfxcom

A Python 3 library for working with your RFXTrx and automating your home.

This library is designed to work on Python 3.3+ and although you can write
alternative transport layers, out of the box it is designed to work with
asyncio.

At the moment this library is relatively new, the number of devices supported
is limited to the devices that @d0ugal owns. The current list includes:

1. Status Packets from the RFXTrx itself.
2. Energy usage sensors (such as the Owl CM119/160 and Owl CM180)
3. Temperature and humidity sensors (such as the Oregon THGN132)


