"""
Config file containing information about the various sensors or systems and how they are connected
to the RPI.
"""

import board

# data from sensors with lower priority values will be processed first
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
        },
    },
    "TEMPERATURES": {
        "priority": 0,
        "read_interval": 0, # delay already created by the conversion time of the sensors
        "name": "TEMPERATURES",
        "sensors": {
            "battery_12V": {"warn": 0, "alert": 0, "max": 0, "address": 0x00000dc67e14},
            "battery_24V": {"warn": 50, "alert": 80, "max": 0, "address": 0x00000e841698},
            # "fc_controllers": {"warn": 0, "alert": 0, "max": 0, "address": 0x000000000000},
            # "h2_plate": {"warn": 0, "alert": 0, "max": 0, "address": 0x000000000000},
            # "h2_tanks": {"warn": 0, "alert": 0, "max": 0, "address": 0x000000000000},
        }
    },
    "BATTERY_GAUGES": {
        "priority": 0,
        "read_interval": 1,
        "name": "BATTERY_GAUGES",
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
        "name": "ACCELEROMETER",
        "i2c_address": 0x53,
    },
    "HMC5883L": {
        "priority": 1,
        "read_interval": 1,
        "name": "COMPASS",
        "i2c_address": 0x0C,
    },
    "ITG3205": {
        "priority": 1,
        "read_interval": 1,
        "name": "GYROSCOPE",
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
        "name": "START_BUTTON",
    },
}

DEVICE_IDS = {
    "FUELCELLS" : 0x00,
    "FUELCELL_A" : 0x01,
    "FUELCELL_B" : 0x02,
    "DCDC_CONVERTER" : 0x04,

    "TEMPERATURES" : 0x10,
    "TEMPERATURE_BATTERY_12V" : 0x11,
    "TEMPERATURE_BATTERY_24V" : 0x12,
    "TEMPERATURE_H2_PLATE" : 0x13,
    "TEMPERATURE_H2_TANKS" : 0x14,
    "TEMPERATURE_FUELCELL_CONTROLLERS" : 0x15,

    "BATTERY_GAUGES" : 0x20,
    "I2C_MULTIPLEX" : 0x21,
    "BATTERY_GAUGE_12V" : 0x22,
    "BATTERY_GAUGE_24V" : 0x23,

    "MANOMETERS" : 0x40,
    "MANOMETER_0" : 0x41,
    "MANOMETER_1" : 0x42,

    "START_BUTTON" : 0x50,
    "PRECHARGE" : 0x51,
    "ACTUATORS" : 0x58,
    "ACTUATOR_1" : 0x59,
    "ACTUATOR_2" : 0x5A,

    "ARDUINO" : 0x60,
    "INTERFACE" : 0x61,
    "RASPBERRY_PI_CPU_TEMPERATURE" : 0x62,

    "TELEMETRY_SENSORS" : 0x70,
    "IMU" : 0x71,
    "GYROSCOPE" : 0x73,
    "COMPASS" : 0x75,
    "ACCELEROMETER" : 0x77,
    "GPS" : 0x78,
}

# Config for telemetry (serial connection over USB with Arduino)
TELE_CONFIG = {
    "serial_port": "/dev/ttyACM0",
}

BUTTON_DEBOUNCE_S = 0.02

ADC_ENABLE_PIN = board.D8

SMBUS_ID = 1
