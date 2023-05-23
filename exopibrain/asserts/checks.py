from asserts.asserts import WarningError, CriticalError
from config import CONFIG

CPU_MAX_TEMP_WARN = 80
CPU_MAX_TEMP_ALERT = 90

def cpu_temp_check(data):
    """
    Checks the CPU temperature.
    """
    temperature = data["temperature"]
    msg = f"CPUTemp: {temperature}"
    if CPU_MAX_TEMP_WARN <= temperature < CPU_MAX_TEMP_ALERT:
        raise WarningError(msg)
    if temperature > CPU_MAX_TEMP_ALERT:
        raise CriticalError(msg)

def fuel_cell_check(data):
    pass

CHECKS = {
    CONFIG["RP_CPU_TEMP"]["name"]: cpu_temp_check,
    CONFIG["FUELCELL_A"]["name"]: fuel_cell_check,
    CONFIG["FUELCELL_B"]["name"]: fuel_cell_check,
}

def get_check(key):
    """
    Returns the check function for the given key.
    """
    if key in CHECKS.keys():
        return CHECKS[key]
    return lambda data: None
