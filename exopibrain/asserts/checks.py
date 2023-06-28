from asserts.asserts import WarningError, CriticalError
from config import CONFIG

CPU_MAX_TEMP_WARN = 80
CPU_MAX_TEMP_ALERT = 90

BATT_MAX_TEMP_WARN = 50
BATT_MAX_TEMP_ALERT = 80

def temperature_check(name, temperature, max_temp_warn, max_temp_alert):
    """
    Checks the temperature of a sensor.
    """
    msg = f"{name}: {temperature}"
    if max_temp_warn <= temperature < max_temp_alert:
        raise WarningError(msg)
    if temperature > max_temp_alert:
        raise CriticalError(msg)
    
def cpu_temp_check(data):
    """
    Checks the CPU temperature.
    """
    temperature = data["temperature"]
    temperature_check(CONFIG["RP_CPU_TEMP"]["name"], temperature, CPU_MAX_TEMP_WARN, CPU_MAX_TEMP_ALERT)

def fuel_cell_check(data):
    # TODO: Implement once we decide what we want to check 
    # (redundancy to what the cell controllers already do)
    pass

def batt_temp_check(data):
    """
    Checks the battery temperature (thermocouple)
    """
    temperature = data["temperature"]
    temperature_check(CONFIG["BATT_TEMP"]["name"], temperature, BATT_MAX_TEMP_WARN, BATT_MAX_TEMP_ALERT)


_CHECKS = {
    CONFIG["RP_CPU_TEMP"]["name"]: cpu_temp_check,
    CONFIG["FUELCELL_A"]["name"]: fuel_cell_check,
    CONFIG["FUELCELL_B"]["name"]: fuel_cell_check,
    CONFIG["BATT_TEMP"]["name"]: batt_temp_check
}

def get_check(key):
    """
    Returns the check function for the given key.
    """
    if key in _CHECKS.keys():
        return _CHECKS[key]
    return lambda data: None
