from fuel_cell.fuel_cell import FuelCell
from fuel_cell.actuators import Actuator
from time import sleep
from gpiozero import Button

class BoatStarter:
    def __init__(self, start_btn_pin, fc_a, fc_b, in_mano, out_mano, in_v: Actuator):
        self.btn = Button(start_btn_pin)
        self.fc_a = fc_a
        self.fc_b = fc_b
        self.in_mano = in_mano
        self.out_mano = out_mano
        self.in_v = in_v
        self.start_success = False
    
    def startup_procedure(self):
        try:
            #inlet_pressure = inlet.get_pressure()
            # Check pressure (between 0.5 and 0.7 bar inlet), check outlet connecté
            #outlet_pressure = outlet.get_pressure()
            self.fc_a.start_fuel_cell()
            sleep(5)
            self.fc_b.start_fuel_cell()
            sleep(5)
            # in_v.open_valve()
            self.start_success = True
        except Exception:
            pass

    def wait_start(self):
        # Should be a blocking method
        self.btn.when_pressed = self.startup_procedure()

    
