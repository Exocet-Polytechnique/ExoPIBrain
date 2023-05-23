CONFIG = {
    "FUELCELL_A": {
        "serial": {
            "serial_port": "/dev/ttyAMA0",
            "baudrate": 57600
        },
        "priority": 0,
        "read_interval": 1,
        "name": "FUELCELL_A"
    },
    "FUELCELL_B": {
        "serial": {
            "serial_port": "/dev/ttyAMA0",
            "baudrate": 57600
        },
        "priority": 0,
        "read_interval": 1,
        "name": "FUELCELL_B"
    },
    "GPS": {
        "serial": {
            "serial_port": "/dev/ttyAMA0",
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
        "name": "IMU"
    },

}