
from time import sleep
from asserts.asserts import StartUpError
from gpiozero import Button

class BoatStarter:
    def __init__(self, start_btn_pin, fc_a, fc_b, in_mano, out_mano, in_v):
        self.btn = Button(start_btn_pin)
        self.fc_a = fc_a
        self.fc_b = fc_b
        self.in_mano = in_mano
        self.out_mano = out_mano
        self.in_v = in_v
        self.start_success = False

    def startup_procedure(self):
        """
        Startup procedure for H2 and fuel cells.
        TODO: Link manometers and actuators to this procedure.
        TODO: Do checks on pressure and temperature.
        """
        try:
            #inlet_pressure = self.in_mano.get_pressure()
            # Check pressure (between 0.5 and 0.7 bar inlet), check outlet connection
            #outlet_pressure = self.out_mano.get_pressure()
            self.fc_a.start_fuel_cell()
            sleep(5)
            self.fc_b.start_fuel_cell()
            sleep(5)
            self.in_v.open_valve()
            self.start_success = True
        except Exception:
            raise StartUpError()

    def wait_for_press(self):
        self.btn.wait_for_press()

if __name__ == "__main__":
    from config import CONFIG
    START_GPIO = 27
    starter = BoatStarter(START_GPIO, None, None, None, None, None)
    print("Waiting for press...")
    starter.wait_for_press()
    print("Button pressed")
    