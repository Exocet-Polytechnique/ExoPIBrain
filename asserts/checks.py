"""
Check functions called when processing the data queue.
"""

from config import CONFIG
from procedures.exception_handling.sensor_result import SensorResult
from procedures.exception_handling.messages import create_message_id, CRITICAL_TEMPERATURE, \
    CRITICAL_CHARGE, ALERT_TEMPERATURE, ALERT_CHARGE, WARNING_TEMPERATURE, WARNING_CHARGE


def check_device_temperature(name, temperature, warning_temperature,
                             alert_temperature, critical_temperature):
    """
    Checks the temperature of a sensor.
    """
    if temperature >= critical_temperature:
        return SensorResult(False, create_message_id(name, CRITICAL_TEMPERATURE))
    if temperature >= alert_temperature:
        return SensorResult(False, create_message_id(name, ALERT_TEMPERATURE))
    if temperature >= warning_temperature:
        return SensorResult(False, create_message_id(name, WARNING_TEMPERATURE))

    return SensorResult(True, temperature)

def check_device_charge(name, charge, warning_charge, alert_charge, critical_charge):
    """
    Checks the charge level of a battery.
    """
    if charge <= critical_charge:
        return SensorResult(False, create_message_id(name, CRITICAL_CHARGE))
    if charge <= alert_charge:
        return SensorResult(False, create_message_id(name, ALERT_CHARGE))
    if charge <= warning_charge:
        return SensorResult(False, create_message_id(name, WARNING_CHARGE))

    return SensorResult(True, charge)


def check_cpu_temperature(data):
    """
    Checks the CPU temperature.
    """
    temperature = data["temperature"]
    return check_device_temperature(
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["name"],
        temperature,
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["warning_temperature"],
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["alert_temperature"],
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["critical_temperature"]
    )


def check_temperatures(data):
    """
    Check temperature from all thermocouples.
    """
    results = []
    for name, temperature in data.items():
        results.append(check_device_temperature(
            name,
            temperature,
            CONFIG["TEMPERATURES"]["sensors"][name]["warn"],
            CONFIG["TEMPERATURES"]["sensors"][name]["alert"],
            CONFIG["TEMPERATURES"]["sensors"][name]["alert"]
        ))

    return results

def check_battery_levels(data):
    """
    Checks the charge level of the batteries
    """
    results = []

    for name, battery in data.items():
        results.append(check_device_charge(
            name,
            battery["charge_level"],
            CONFIG["BATTERY_GAUGES"]["charge_levels"][name]["warning"],
            CONFIG["BATTERY_GAUGES"]["charge_levels"][name]["alert"],
            CONFIG["BATTERY_GAUGES"]["charge_levels"][name]["critical"]
        ))

    return results

def check_fuel_cell(data):
    # TODO: figure out something to check. This function is here for redundency, but the fuel cell
    # controllers should already immplement some security.
    return SensorResult(True, None)


# List of sensors we want to check as well as their respective functions
_CHECKS = {
    CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["name"]: check_cpu_temperature,
    CONFIG["TEMPERATURES"]["name"]: check_temperatures,
    CONFIG["FUELCELL_A"]["name"]: check_fuel_cell,
    CONFIG["FUELCELL_B"]["name"]: check_fuel_cell,
    CONFIG["BATTERY_GAUGES"]["name"]: check_battery_levels,
}

def perform_check(name, data):
    """
    Check a sensor for any problems. This function will raise a `WarningError` or `CriticalError`
    if a problem is detected.
    """
    if name in _CHECKS:
        return _CHECKS[name](data)

    return SensorResult(True, data)
