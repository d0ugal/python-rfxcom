
class RFXComException(Exception):
    pass


class PacketHandlerNotFound(RFXComException):
    """This exception is raised when no handler is provided to the transport
    layer for a particular packet and thus it can't be handled.
    """


class InvalidPacketLength(RFXComException):
    """This exception is raised when the length of the packet doesn't match
    the length given in the first byte of the packet. This then means we
    either have too many or too few bytes.
    """


class UnknownPacketType(RFXComException):
    """This exception is raised when the packet type isn't recognised by the
    used packet handler class.
    """


class UnknownPacketSubtype(RFXComException):
    """This exception is raised when the packet subtype isn't recognised by
    the used packet handler class.
    """
