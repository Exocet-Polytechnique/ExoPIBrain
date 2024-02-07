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
        "sensors": {"M0": (0, 400)},
    },
    "TEMPERATURES": {
        "priority": 0,
        "read_interval": 0, # delay already created by the conversion time of the sensors
        "name": "TEMPERATURES",
        "sensors": {
            # (warning_temperature, alert_temperature, max_temperature)
            "battery_12V": (0, 0, 0),
            "battery_24V": (50, 80, 0),
            "fc_controllers": (0, 0, 0),
            "h2_plate": (0, 0, 0),
            "h2_tanks": (0, 0, 0),
        }
    },
    "IMU": {
        "priority": 1,
        "read_interval": 1,
        "name": "IMU",
        "new_rev_i2c_id": 1,
        "old_rev_i2c_id": 0,
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
    "RP_CPU_TEMP": {
        "priority": 2,
        "read_interval": 5,
        "name": "RP_CPU_TEMP",
    },
    "START_BUTTON": {
        "pin": 27,
    },
}

# Config for telemetry (serial connection over USB with Arduino)
TELE_CONFIG = {
    "serial_port": "/dev/ttyACM0",
}
