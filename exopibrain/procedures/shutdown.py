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
    """
    PURGE PROCEDURE:
    1. Close H2 inlet valve
    2. Open H2 outlet valve
    3. Open H2 purge valve
    4. Send START command to fuel cell. Wait for response
    5. Repeat steps 4-5 for second fuel cell
    6. Close H2 outlet valve
    7. Close H2 purge valve
    """
    success = True
    try:
        in_v.close_valve()
        out_v.open_valve()
        he_v.open_valve()
        fc_a.start_fuel_cell()
        fc_b.start_fuel_cell()
        out_v.close_valve()
        he_v.close_valve()
    except Exception:
        success = False
    return success
    