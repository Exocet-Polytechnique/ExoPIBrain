"""
Defines the messages used in the exception handling procedures.

See: https://github.com/Exocet-Polytechnique/ExoPIBrain/wiki/Format-&-gestion-d'erreurs
"""

from config import CONFIG, DEVICE_IDS
from utils import to_uint16

SEVERITY_MASK = 0xFF00
SEVERITY_BITSHIFT = 8
DEVICE_ID_MASK = 0x00FF

PERMANENT_MESSAGE_TIME = -1
DEFAULT_MESSAGE_TIME = 3
TEMPERATURE_WARNING_REFRESH = 5

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


def get_message_severity(message_id):
    """
    Gets the message severity from a message id.

    Args:
        message_id (int): The message id.

    Returns:
        int: The message severity.
    """
    return (message_id & SEVERITY_MASK) >> SEVERITY_BITSHIFT

def get_message_device_id(message_id):
    """
    Gets the device id from a message id.

    Args:
        message_id (int): The message id.

    Returns:
        int: The device id.
    """
    return message_id & DEVICE_ID_MASK


# 1. Common exceptions (some define the end of ranges)
# The values are arbirary, although messages with higher severity have lower values

CRITICAL_ERROR_EXIT   = 0x10

CRITICAL_TEMPERATURE  = 0x11
CRITICAL_CHARGE       = 0x12
CRITICAL_ERROR        = 0x30

ALERT_TEMPERATURE     = 0x31
ALERT_CHARGE          = 0x32
ERROR_DISCONNECTED    = 0x40
ERROR                 = 0x50

WARNING_TEMPERATURE   = 0x51
WARNING_CHARGE        = 0x52
WARNING_BAD_DATA      = 0x70
WARNING               = 0xA0

INFO_CONNECTED        = 0xA1
INFO                  = 0xC0


# 2. Some common message ids

BATTERY_12V_CRITICAL_CHARGE = create_message_id("BATTERY_GAUGE_12V", CRITICAL_CHARGE)
BATTERY_12V_ALERT_CHARGE = create_message_id("BATTERY_GAUGE_12V", ALERT_CHARGE)
BATTERY_12V_WARNING_CHARGE = create_message_id("BATTERY_GAUGE_12V", WARNING_CHARGE)
BATTERY_24V_CRITICAL_CHARGE = create_message_id("BATTERY_GAUGE_24V", ALERT_CHARGE)
BATTERY_24V_ALERT_CHARGE = create_message_id("BATTERY_GAUGE_24V", ALERT_CHARGE)
BATTERY_24V_WARNING_CHARGE = create_message_id("BATTERY_GAUGE_24V", WARNING_CHARGE)

GPS_WARNING_POOR_CONNECTION = create_message_id("GPS", WARNING_BAD_DATA)


# 3. Messages

MESSAGES_CONFIG = {
    # TODO: add more messages as we go

    BATTERY_12V_CRITICAL_CHARGE:
        ("Critical: 12V battery charge level is critically low. Shutting down.",
          PERMANENT_MESSAGE_TIME),
    BATTERY_12V_ALERT_CHARGE:
        ("Alert: 12V battery charge level is critically low. Return to dock IMMEDIATLY.",
          PERMANENT_MESSAGE_TIME),
    BATTERY_12V_WARNING_CHARGE:
        ("Warning: 12V battery charge level is low.", PERMANENT_MESSAGE_TIME),
    BATTERY_24V_CRITICAL_CHARGE:
        ("Critical: 24V battery charge level is critically low. Shutting down",
          PERMANENT_MESSAGE_TIME),
    BATTERY_24V_ALERT_CHARGE:
        ("Alert: 24V battery charge level is critically low. Return to dock IMMEDIATLY.",
          PERMANENT_MESSAGE_TIME),
    BATTERY_24V_WARNING_CHARGE:
        ("Warning: 24V battery charge level is low.", PERMANENT_MESSAGE_TIME),

    GPS_WARNING_POOR_CONNECTION:
        ("Poor GPS connection; no data is being received.", CONFIG["GPS"]["read_interval"]),
}

DEFAULT_EXCEPTION_MESSAGES = {
    CRITICAL_ERROR_EXIT:
        ("Critical error. Pilot must LEAVE the boat IMMEDIATLY.", PERMANENT_MESSAGE_TIME),
    CRITICAL_TEMPERATURE: ("Critical temperature detected.", PERMANENT_MESSAGE_TIME),
    CRITICAL_CHARGE:
        ("Critical charge level detected. Boat will shutdown.", PERMANENT_MESSAGE_TIME),
    CRITICAL_ERROR: ("Critical error. Boat shutting down.", PERMANENT_MESSAGE_TIME),

    ALERT_TEMPERATURE:
        ("Very high temperature detected. Return to dock IMMEDIATLY.", PERMANENT_MESSAGE_TIME),
    ALERT_CHARGE:
        ("Battery charge level very low. Return to dock IMMEDIATLY.", PERMANENT_MESSAGE_TIME),
    ERROR_DISCONNECTED: ("A sensor has been disconnected.", PERMANENT_MESSAGE_TIME),
    ERROR: ("Unkown error signal received", PERMANENT_MESSAGE_TIME),

    WARNING_TEMPERATURE: ("High temperature detected.", TEMPERATURE_WARNING_REFRESH),
    WARNING_CHARGE:
        ("Low battery charge level detected.", PERMANENT_MESSAGE_TIME),
    WARNING_BAD_DATA:
        ("Invalid data received.", DEFAULT_MESSAGE_TIME),
    WARNING: ("Unkown warning signal received.", DEFAULT_MESSAGE_TIME),

    INFO_CONNECTED: ("Sensor connected.", DEFAULT_MESSAGE_TIME),
    INFO: ("Unkown info signal received.", DEFAULT_MESSAGE_TIME),
}
