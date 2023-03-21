from asserts.asserts import AlertError, CriticalError

CPU_MAX_TEMP_WARN = 80
CPU_MAX_TEMP_ALERT = 90
def cpu_temp_check(temperature):
    msg = f"CPUTemp: {temperature}"
    if CPU_MAX_TEMP_WARN <= temperature < CPU_MAX_TEMP_ALERT:
        raise AlertError(msg)
    if temperature > CPU_MAX_TEMP_ALERT:
        raise CriticalError(msg)

def fuel_cell_check(data):
    pass

CHECKS = {
    "CPU_t": cpu_temp_check,
    "FuelCell": fuel_cell_check,
    
}

def get_check(key):
    return CHECKS[key]
