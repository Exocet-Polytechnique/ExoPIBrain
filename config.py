"""
Config file containing information about the various sensors or systems and how they are connected
to the RPI.

NOTE: A lower priority value means that the data coming from these sensors will be processed first.
"""

CONFIG = {
    "FUELCELL_A": {
        "serial": {
            "port": "/dev/tty_FCA",  # Ports on the RP have been renamed to tty_FCA and tty_FCB
            "baudrate": 57600,
        },
        "priority": 0,
        "read_interval": 1,
        "name": "FUELCELL_A",
    },
    "FUELCELL_B": {
        "serial": {
            "port": "/dev/tty_FCB",
            "baudrate": 57600,
        },
        "priority": 0,
        "read_interval": 1,
        "name": "FUELCELL_B",
    },
    "MANOMETERS": {
        "priority": 0,
        "read_interval": 1,
        "name": "MANOMETERS",
        "sensors": {
            "M0": {"range": (0, 400), "channel": 0},
            "M1": {"range": (0, 4), "channel": 1},
        },
    },
    "TEMPERATURES": {
        "priority": 0,
        "read_interval": 0, # delay already created by the conversion time of the sensors
        "name": "TEMPERATURES",
        "sensors": {
            "H2_plate": {"warn": 0, "alert": 0, "max": 0, "address": 0x00000dc67e14},
            "refuelling_station": {"warn": 50, "alert": 80, "max": 0, "address": 0x00000e841698},
            "floating": {"warn": 0, "alert": 0, "max": 0, "address": 0x00000dc6d911},
            # "h2_plate": {"warn": 0, "alert": 0, "max": 0, "address": 0x000000000000},
            # "h2_tanks": {"warn": 0, "alert": 0, "max": 0, "address": 0x000000000000},
        }
    },
    "BATT_GAUGES": {
        "priority": 0,
        "read_interval": 1,
        "name": "BATT_GAUGES",
        "i2c_address": 0x64,
        "select_gpio": 13,
        "charge_levels" : {
            # coulomb counter values - these will definitely need to be adjusted
            "12V": {
                "warning": 1000,
                "alert": 1500,
            },
            "24V": {
                "warning": 1000,
                "alert": 1500,
            }
        }
    },
    "ADXL345": {
        "priority": 1,
        "read_interval": 1,
        "name": "Accelerometer",
        "i2c_address": 0x53,
    },
    "HMC5883L": {
        "priority": 1,
        "read_interval": 1,
        "name": "Compass",
        "i2c_address": 0x0C,
    },
    "ITG3205": {
        "priority": 1,
        "read_interval": 1,
        "name": "Gyroscope",
        "i2c_address": 0x68,
    },
    "GPS": {
        "serial": {
            "port": "/dev/tty0",
            "baudrate": 9600,
        },
        "priority": 1,
        "read_interval": 3,
        "name": "GPS",
    },
    "RASPBERRY_PI_CPU_TEMPERATURE": {
        "priority": 2,
        "read_interval": 5,
        "name": "RASPBERRY_PI_CPU_TEMPERATURE",
        "warning_temperature": 80,
        "alert_temperature": 90,
    },
    "START_BUTTON": {
        "pin": 27,
    },
    "PRECHARGE" : {
        "main_contactor" : 22,
        "stage1_contactor" : 27,
        "stage2_contactor" : 17,
    },
    "ACTUATORS": {
        "valve1": {
            "output_pin": 23,
            "error_pin": 5,
            "closed_on_low": True, # NOTE: verify before tests
        },
        "valve2": {
            "output_pin": 24,
            "error_pin": 6,
            "closed_on_low": True, # NOTE: verify before tests
        },
    }
}

# Config for telemetry (serial connection over USB with Arduino)
TELE_CONFIG = {
    "serial_port": "/dev/ttyACM0",
}

BUTTON_DEBOUNCE_S = 0.02

import board
ADC_ENABLE_PIN = board.D8

SMBUS_ID = 1
