"""
Check functions called when processing the data queue.
"""

from config import CONFIG
from procedures.exception_handling.sensor_result import SensorResult
from procedures.exception_handling.messages import create_message_id, WARNING_TEMPERATURE, \
    CRITICAL_TEMPERATURE, BATTERY_12V_CRITICAL_CHARGE, BATTERY_12V_WARNING_CHARGE, \
    BATTERY_24V_CRITICAL_CHARGE, BATTERY_24V_WARNING_CHARGE


def check_device_temperature(name, temperature, max_temperature_warn, max_temperature_alert):
    """
    Checks the temperature of a sensor.
    """
    if max_temperature_warn <= temperature < max_temperature_alert:
        return SensorResult(False, create_message_id(name, WARNING_TEMPERATURE))
    if temperature > max_temperature_alert:
        return SensorResult(False, create_message_id(name, CRITICAL_TEMPERATURE))

    return SensorResult(True, None)


def check_cpu_temperature(data):
    """
    Checks the CPU temperature.
    """
    temperature = data["temperature"]
    return check_device_temperature(
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["name"],
        temperature,
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["warning_temperature"],
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["alert_temperature"]
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
            CONFIG["TEMPERATURES"]["sensors"][name]["alert"]
        ))

    return results

def check_battery_levels(data):
    """
    Checks the charge level of the batteries
    """
    results = []

    battery_charge_12V = data["12V"]["charge_level"]

    # This will ultimately be changed when we implement proper error checking and protocols.
    # We should also check the batteries individually, but this will do for now.
    if battery_charge_12V >= CONFIG["BATTERY_GAUGES"]["charge_levels"]["12V"]["alert"]:
        results.append(SensorResult(False, BATTERY_12V_CRITICAL_CHARGE))
    elif battery_charge_12V >= CONFIG["BATTERY_GAUGES"]["charge_levels"]["12V"]["warning"]:
        results.append(SensorResult(False, BATTERY_12V_WARNING_CHARGE))

    battery_charge_24V = data["24V"]["charge_level"]

    if battery_charge_24V >= CONFIG["BATTERY_GAUGES"]["charge_levels"]["24V"]["alert"]:
        results.append(SensorResult(False, BATTERY_24V_CRITICAL_CHARGE))
    elif battery_charge_24V >= CONFIG["BATTERY_GAUGES"]["charge_levels"]["24V"]["warning"]:
        results.append(SensorResult(False, BATTERY_24V_WARNING_CHARGE))

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

    return SensorResult(True, None)
