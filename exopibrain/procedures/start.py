from fuel_cell.fuel_cell import FuelCell
from fuel_cell.actuators import Actuator
from time import sleep

def start_boat(fc_a: FuelCell, fc_b: FuelCell, in_press, out_press, in_v: Actuator):
    """
    START PROCEDURE:
    1. Check pressure (between 0.5 and 0.7 bar inlet), check outlet connecté
    2. Check battery charge
    3. BAUD rate 57600 for both fuel cells
    4. Low tension sends 24V for cell startup, wait at least 5sec
    5. Send START command to fuel cell. Wait for response
    6. Repeat steps 4-5 for second fuel cell
    7. Open H2 valve (inlet)
    8. Start reading loop for all fuel cells
    """
    success = True
    try:
        #inlet_pressure = inlet.get_pressure()
        # Check pressure (between 0.5 and 0.7 bar inlet), check outlet connecté
        #outlet_pressure = outlet.get_pressure()
        fc_a.start_fuel_cell()
        sleep(5)
        fc_b.start_fuel_cell()
        sleep(5)
        # in_v.open_valve()
    except Exception:
        success = False
    return success
    
