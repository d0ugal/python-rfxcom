"""
Interface Message
=================

"""

from rfxcom.protocol.base import BasePacketHandler


_MSG1_RECEIVER_TYPE = {
    0x50: '310MHz',
    0x51: '315MHz',
    0x52: '433.92MHz receiver only',
    0x53: '433.92MHz transceiver',
    0x55: '868.00MHz',
    0x56: '868.00MHz FSK',
    0x57: '868.30MHz',
    0x58: '868.30MHz FSK',
    0x59: '868.35MHz',
    0x5A: '868.35MHz FSK',
    0x5B: '868.95MHz',
}

#: Three lists defining the different supported devices. The names as msg3-5
#: as messages 3 to 6 out of a larger list of messages in the packet define the
#: protocols. Each one then maps to a binary flag in a series of three bytes.
_MSG3_PROTOCOLS = [
    'Display undecoded',
    'RFU6',
    'Byron SX',
    'RSL',
    'Lighting4',
    'FineOffset/Viking',
    'Rubicson',
    'AE Blyss',
]

_MSG4_PROTOCOLS = [
    'BlindsT1/T2/T3/T4',
    'BlindsT0',
    'ProGuard',
    'FS20',
    'La Crosse',
    'Hideki/UPM',
    'AD LightwaveRF',
    'Mertik',
]

_MSG5_PROTOCOLS = [
    'Visonic',
    'ATI',
    'Oregon Scientific',
    'Meiantech',
    'HomeEasy EU',
    'AC',
    'ARC',
    'X10',
]

PROTOCOLS = _MSG3_PROTOCOLS + _MSG4_PROTOCOLS + _MSG5_PROTOCOLS


class Status(BasePacketHandler):
    """The Status packet is returned by the RFXtrx itself and is used to show
    the status and configuration of the device.

    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x0A (excludes this byte)
    1       Packet Type, 0x14
    2       Sub Type
    3       Sequence Number
    4       Command
    5       Transceiver Type
    6       Firmware Version
    7       Flags for the enabled devides defined in _MSG3_PROTOCOLS
    8       Flags for the enabled devides defined in _MSG4_PROTOCOLS
    9       Flags for the enabled devides defined in _MSG5_PROTOCOLS
    10      Message 6
    11      Message 7
    12      Message 8
    13      Message 9
    ====    ====
    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x01: "Interface message"
        }
        self.SUB_TYPES = {
            0x00: "Response on a mode command",
            0xFF: "Wrong command received from the application.",
        }

    def _log_enabled_protocols(self, flags, protocols):
        """Given a list of single character strings of 1's and 0's and a list
        of protocol names. Log the status of each protocol where ``"1"`` is
        enabled and ``"0"`` is disabled. The order of the lists here is
        important as they need to be zipped together to create the mapping.
        Then return a tuple of two lists containing the names of the enabled
        and disabled protocols.

        :param character: A list of single character strings of 1's and 0's
        :type character: list

        :param protocols: A list of protocol names.
        :type protocols: list

        :return: Tuple containing two lists which contain n strings.
        :rtype: tuple
        """

        enabled, disabled = [], []

        for procol, flag in sorted(zip(protocols, flags)):

            if flag == '1':
                enabled.append(procol)
                status = 'Enabled'
            else:
                disabled.append(procol)
                status = 'Disabled'

            message = "{0:21}: {1}".format(procol, status)
            self.log.info(message)

        return enabled, disabled

    def _int_to_binary_list(self, int_):
        """A helper function that given an integer will return the eight byte
        binary representation as a list.

        :param data: Integer to be converted
        :type data: int

        :return: A list of single character strings of 1's and 0's
        :rtype: list
        """
        return list('{0:08b}'.format(int_))

    def parse(self, data):
        """Parse a 13 byte packet in the Status format.

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        packet_length = data[0]
        packet_type = data[1]
        sub_type = data[2]
        sequence_number = data[3]
        command_type = data[4]
        transceiver_type = data[5]
        transceiver_type_text = _MSG1_RECEIVER_TYPE.get(data[5])
        firmware_version = data[6]

        flags = self._int_to_binary_list(data[7])
        flags.extend(self._int_to_binary_list(data[8]))
        flags.extend(self._int_to_binary_list(data[9]))

        enabled, disabled = self._log_enabled_protocols(flags, PROTOCOLS)

        return {
            'packet_length': packet_length,
            'packet_type': packet_type,
            'packet_type_name': self.PACKET_TYPES.get(packet_type),
            'sequence_number': sequence_number,
            'sub_type': sub_type,
            'sub_type_name': self.SUB_TYPES.get(sub_type),
            'command_type': command_type,
            'transceiver_type': transceiver_type,
            'transceiver_type_text': transceiver_type_text,
            'firmware_version': firmware_version,
            'enabled_protocols': enabled,
            'disabled_protocols': disabled,
        }
