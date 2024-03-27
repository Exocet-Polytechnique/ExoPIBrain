"""
Defines the messages used in the exception handling procedures.

See: https://github.com/Exocet-Polytechnique/ExoPIBrain/wiki/Format-&-gestion-d'erreurs
"""

from config import CONFIG, DEVICE_IDS
from utils import to_uint16

def create_message_id(device, severity):
    """
    Creates a message id from the device and severity.

    Args:
        device (str or int): The name or id of the device.
        severity (int): The severity of the message.

    Returns:
        int: The message id.
    """

    if isinstance(device, str):
        device = DEVICE_IDS[device]

    return to_uint16(severity, device)


# 1. Common exceptions (some define the start of ranges)

CRITICAL_ERROR_EXIT = 0x00
CRITICAL_ERROR      = 0x01

CONNECTED           = 0x10
DISCONNECTED        = 0x11

WARNING             = 0x20

INFO                = 0xA0


# 2. Fixed message ids

GPS_WARNING_POOR_CONNECTION = create_message_id("GPS", WARNING + 3)


# 3. Messages

MESSAGES_CONFIG = {
    # TODO: add more messages as we go

    GPS_WARNING_POOR_CONNECTION:
        ("Poor GPS connection; no data is being received.", CONFIG["GPS"]["read_interval"] + 1),
}

DEFAULT_EXCEPTION_MESSAGES = {
    CRITICAL_ERROR_EXIT: ("Critical error. Pilot must LEAVE the boat IMMEDIATLY.", -1),
    CRITICAL_ERROR: ("Critical error. Boat shutting down.", -1),

    CONNECTED: ("Sensor connected.", 3),
    DISCONNECTED: ("Sensor disconnected.", 3),

    WARNING: ("Unkown warning signal received.", 3),
}
