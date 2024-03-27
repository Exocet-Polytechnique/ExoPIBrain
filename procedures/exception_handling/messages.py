"""
Defines the messages used in the exception handling procedures.

See: https://github.com/Exocet-Polytechnique/ExoPIBrain/wiki/Format-&-gestion-d'erreurs
"""

from config import CONFIG

# 1. Devices

FUELCELLS                        = 0x00
FUELCELL_A                       = 0x01
FUELCELL_B                       = 0x02
DCDC_CONVERTER                   = 0x04

TEMPERATURES                     = 0x10
TEMPERATURE_BATTERY_12V          = 0x11
TEMPERATURE_BATTERY_24V          = 0x12
TEMPERATURE_H2_PLATE             = 0x13
TEMPERATURE_H2_TANKS             = 0x14
TEMPERATURE_FUELCELL_CONTROLLERS = 0x15

BATTERY_GAUGES                   = 0x20
I2C_MULTIPLEX                    = 0x21
BATTERY_GAUGE_12V                = 0x22
BATTERY_GAUGE_24V                = 0x23

MANOMETERS                       = 0x40
MANOMETER_0                      = 0x41
MANOMETER_1                      = 0x42

START_BUTTON                     = 0x50
PRECHARGE                        = 0x51
ACTUATORS                        = 0x58
ACTUATOR_1                       = 0x59
ACTUATOR_2                       = 0x5A

ARDUINO                          = 0x60
INTERFACE                        = 0x61
CPU_TEMPERATURE                  = 0x62

TELEMETRY_SENSORS                = 0x70
IMU                              = 0x71
GYROSCOPE                        = 0x73
COMPASS                          = 0x75
ACCELEROMETER                    = 0x77
GPS                              = 0x78


# 2. Common exceptions (some define the start of ranges)

CRITICAL_ERROR_EXIT = 0x00
CRITICAL_ERROR      = 0x01

CONNECTED           = 0x10
DISCONNECTED        = 0x11

WARNING             = 0x20

INFO                = 0xA0


# 3. Message ids

GPS_WARNING_POOR_CONNECTION = 0x2320


# 4. Messages

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
