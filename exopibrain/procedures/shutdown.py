from fuel_cell.fuel_cell import FuelCell
from fuel_cell.actuators import Actuator

def normal_shutdown(fc_a: FuelCell, fc_b: FuelCell, in_v: Actuator, out_v: Actuator):
    """
    SHUTDOWN PROCEDURE:
    1. Envoi signal END to both fuel cells, wait for response
    2. Close H2 inlet valve
    3. Shutdown battery (contactor)
    """
    success = True
    try:
        fc_a.shutdown_fuel_cell()
        fc_b.shutdown_fuel_cell()
        in_v.close_valve()
        out_v.close_valve()
    except Exception:
        success = False
    return success

def purge_h2(fc_a: FuelCell, fc_b: FuelCell, in_v: Actuator, out_v: Actuator, he_v: Actuator):
    pass