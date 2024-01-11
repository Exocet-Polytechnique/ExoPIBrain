CONFIG = {
    "FUELCELL_A": {
        "serial": {
            "port": "/dev/tty_FCA", # Ports on the RP have been renamed to tty_FCA and tty_FCB
            "baudrate": 57600
        },
        "priority": 0,
        "read_interval": 1,
        "name": "FUELCELL_A"
    },
    "FUELCELL_B": {
        "serial": {
            "port": "/dev/tty_FCB",
            "baudrate": 57600
        },
        "priority": 0,
        "read_interval": 1,
        "name": "FUELCELL_B"
    },
    "GPS": {
        "serial": {
            "port": "/dev/tty0",
            "baudrate": 9600
        },
        "priority": 1,
        "read_interval": 3,
        "name": "GPS"
    },
    "RP_CPU_TEMP": {
        "priority": 2,
        "read_interval": 5,
        "name": "RP_CPU_TEMP"
    },
    "IMU": {
        "priority": 1,
        "read_interval": 1,
        "name": "IMU",
        "new_rev_i2c_id": 1,
        "old_rev_i2c_id": 0,
    },

    "BATT_TEMP": {
        "priority": 0,
        "read_interval": 1,
        "name": "BATT_TEMP"
    }
}

# Config for telemetry
TELE_CONFIG = {
    "serial_port": "/dev/ttyACM0",
}