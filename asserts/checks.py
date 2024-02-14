from asserts.asserts import WarningError, CriticalError
from config import CONFIG

# Maximum temperatures we can reach before the boat is at risk
CPU_MAX_TEMP_WARN = 80
CPU_MAX_TEMP_ALERT = 90


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


def temp_check(data):
    """
    Check temperature from all thermocouples.
    """
    for name, temperature in data.items():
        temperature_check(
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
    if battery_charge_12V >= CONFIG["BATT_GAUGES"]["charge_levels"]["12V"]["alert"]:
        raise CriticalError("Error: 12V battery charge level is critically low.")
    if battery_charge_12V >= CONFIG["BATT_GAUGES"]["charge_levels"]["12V"]["warning"]:
        raise WarningError("Warning: 12V battery charge level is low.")

    battery_charge_24V = data["24V"]["charge_level"]

    if battery_charge_24V >= CONFIG["BATT_GAUGES"]["charge_levels"]["24V"]["alert"]:
        raise CriticalError("Error: 24V battery charge level is critically low.")
    if battery_charge_24V >= CONFIG["BATT_GAUGES"]["charge_levels"]["24V"]["warning"]:
        raise WarningError("Warning: 24V battery charge level is low.")

def fuel_cell_check(data):
    # TODO: figure out something to check. This function is here for redundency, but the fuel cell
    # controllers should already immplement some security.
    pass


# List of sensors we want to check as well as their respective functions
_CHECKS = {
    CONFIG["RP_CPU_TEMP"]["name"]: cpu_temp_check,
    CONFIG["TEMPERATURES"]["name"]: temp_check,
    CONFIG["FUELCELL_A"]["name"]: fuel_cell_check,
    CONFIG["FUELCELL_B"]["name"]: fuel_cell_check,
    CONFIG["BATT_GAUGES"]["name"]: check_battery_levels,
}

def perform_check(name, data):
    """
    Check a sensor for any problems. This function will raise a `WarningError` or `CriticalError`
    if a problem is detected.
    """
    if name in _CHECKS.keys():
        _CHECKS[name](data)
