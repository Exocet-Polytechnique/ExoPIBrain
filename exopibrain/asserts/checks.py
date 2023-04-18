from asserts.asserts import AlertError, CriticalError
from config import CONFIG

CPU_MAX_TEMP_WARN = 80
CPU_MAX_TEMP_ALERT = 90

def cpu_temp_check(data):
    temperature = data["temperature"]
    msg = f"CPUTemp: {temperature}"
    if CPU_MAX_TEMP_WARN <= temperature < CPU_MAX_TEMP_ALERT:
        raise AlertError(msg)
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
    return CHECKS[key]
