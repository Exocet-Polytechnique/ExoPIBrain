from asserts.asserts import WarningError, CriticalError
from config import CONFIG

# Maximum temperatures we can reach before the boat is at risk
CPU_MAX_TEMP_WARN = 80
CPU_MAX_TEMP_ALERT = 90
BATT_MAX_TEMP_WARN = 50
BATT_MAX_TEMP_ALERT = 80


def temperature_check(name, temperature, max_temp_warn, max_temp_alert):
    """
    Checks the temperature of a sensor.
    """
    msg = f"{name}: {temperature}."

    if max_temp_warn <= temperature < max_temp_alert:
        raise WarningError(msg)
    if temperature > max_temp_alert:
        raise CriticalError(msg)
    

def cpu_temp_check(data):
    """
    Checks the CPU temperature.
    """
    temperature = data["temperature"]
    temperature_check(
        CONFIG["RP_CPU_TEMP"]["name"],
        temperature,
        CPU_MAX_TEMP_WARN,
        CPU_MAX_TEMP_ALERT
    )


def batt_temp_check(data):
    """
    Checks the battery temperature (thermocouple)
    """
    temperature = data["temperature"]
    temperature_check(
        CONFIG["BATT_TEMP"]["name"],
        temperature,
        BATT_MAX_TEMP_WARN,
        BATT_MAX_TEMP_ALERT
    )


def fuel_cell_check(data):
    # TODO: figure out something to check. This function is here for redundency, but the fuel cell
    # controllers should already immplement some security.
    pass


# List of sensors we want to check as well as their respective functions
_CHECKS = {
    CONFIG["RP_CPU_TEMP"]["name"]: cpu_temp_check,
    CONFIG["BATT_TEMP"]["name"]: batt_temp_check,
    CONFIG["FUELCELL_A"]["name"]: fuel_cell_check,
    CONFIG["FUELCELL_B"]["name"]: fuel_cell_check,
}

def perform_check(name, data):
    """
    Check a sensor for any problems. This function will raise a `WarningError` or `CriticalError`
    if a problem is detected.
    """
    if name in _CHECKS.keys():
        _CHECKS[name](data)
