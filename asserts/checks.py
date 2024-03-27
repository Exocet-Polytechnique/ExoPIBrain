from asserts.asserts import WarningError, CriticalError
from config import CONFIG


def check_device_temperature(name, temperature, max_temperature_warn, max_temperature_alert):
    """
    Checks the temperature of a sensor.
    """
    msg = f"{name}: {temperature}."

    if max_temperature_warn <= temperature < max_temperature_alert:
        raise WarningError(msg)
    if temperature > max_temperature_alert:
        raise CriticalError(msg)
    

def check_cpu_temperature(data):
    """
    Checks the CPU temperature.
    """
    temperature = data["temperature"]
    check_device_temperature(
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["name"],
        temperature,
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["warning_temperature"],
        CONFIG["RASPBERRY_PI_CPU_TEMPERATURE"]["alert_temperature"]
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

def check_battery_levels(data):
    """
    Checks the charge level of the batteries
    """
    battery_charge_12V = data["12V"]["charge_level"]

    # This will ultimately be changed when we implement proper error checking and protocols.
    # We should also check the batteries individually, but this will do for now.
    if battery_charge_12V >= CONFIG["BATTERY_GAUGES"]["charge_levels"]["12V"]["alert"]:
        raise CriticalError("Error: 12V battery charge level is critically low.")
    if battery_charge_12V >= CONFIG["BATTERY_GAUGES"]["charge_levels"]["12V"]["warning"]:
        raise WarningError("Warning: 12V battery charge level is low.")

    battery_charge_24V = data["24V"]["charge_level"]

    if battery_charge_24V >= CONFIG["BATTERY_GAUGES"]["charge_levels"]["24V"]["alert"]:
        raise CriticalError("Error: 24V battery charge level is critically low.")
    if battery_charge_24V >= CONFIG["BATTERY_GAUGES"]["charge_levels"]["24V"]["warning"]:
        raise WarningError("Warning: 24V battery charge level is low.")

def check_fuel_cell(data):
    # TODO: figure out something to check. This function is here for redundency, but the fuel cell
    # controllers should already immplement some security.
    pass


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
    if name in _CHECKS.keys():
        _CHECKS[name](data)
