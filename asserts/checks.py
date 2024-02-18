from asserts.asserts import WarningError, CriticalError
from config import CONFIG


def check_device_temperature(name, temperature, max_temp_warn, max_temp_alert):
    """
    Checks the temperature of a sensor.
    """
    msg = f"{name}: {temperature}."

    if max_temp_warn <= temperature < max_temp_alert:
        raise WarningError(msg)
    if temperature > max_temp_alert:
        raise CriticalError(msg)
    

def check_cpu_temperature(data):
    """
    Checks the CPU temperature.
    """
    temperature = data["temperature"]
    check_device_temperature(
        CONFIG["RP_CPU_TEMP"]["name"],
        temperature,
        CONFIG["RP_CPU_TEMP"]["warning_temperature"],
        CONFIG["RP_CPU_TEMP"]["alert_temperature"]
    )


def check_temperatures(data):
    """
    Check temperature from all thermocouples.
    """
    for name, temperature in data.items():
        check_device_temperature(
            name,
            temperature,
            CONFIG["TEMPERATURES"]["sensors"][name]["warn"],
            CONFIG["TEMPERATURES"]["sensors"][name]["alert"]
        )


def check_fuel_cell(data):
    # TODO: figure out something to check. This function is here for redundency, but the fuel cell
    # controllers should already immplement some security.
    pass


# List of sensors we want to check as well as their respective functions
_CHECKS = {
    CONFIG["RP_CPU_TEMP"]["name"]: check_cpu_temperature,
    CONFIG["TEMPERATURES"]["name"]: check_temperatures,
    CONFIG["FUELCELL_A"]["name"]: check_fuel_cell,
    CONFIG["FUELCELL_B"]["name"]: check_fuel_cell,
}

def perform_check(name, data):
    """
    Check a sensor for any problems. This function will raise a `WarningError` or `CriticalError`
    if a problem is detected.
    """
    if name in _CHECKS.keys():
        _CHECKS[name](data)
