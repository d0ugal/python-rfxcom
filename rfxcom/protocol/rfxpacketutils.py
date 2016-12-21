
# ----------------------------------------------------------------------------


class RfxPacketUtils:
    """Utility class that offers common services to decode RFX packets
    """

    @staticmethod
    def parse_signal_and_battery(byte):
        """Decode signal/battery byte:
        - 4 upper bits: signal level
        - 4 lower bits: battery level
        """
        rssi = byte >> 4
        battery = byte & 0x0f

        return {
            'signal_level': rssi,
            'battery_level': battery
        }

    @staticmethod
    def parse_signal_upper(byte):
        """Decode signal byte (data in upper bits):
        - 4 upper bits: signal level
        """
        rssi = byte >> 4

        return {
            'signal_level': rssi
        }
