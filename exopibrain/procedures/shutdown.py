from fuel_cell.fuel_cell import FuelCell
from fuel_cell.actuators import Actuator
from gpiozero import Button
from asserts.asserts import ShutDownError
from multithreading.thread import LoopingThread

class BoatStopper:
    def __init__(self, btn_stop_pin, fc_a: FuelCell, fc_b: FuelCell, in_v: Actuator, out_v: Actuator):
        self.btn = Button(btn_stop_pin)
        self.fc_a = fc_a
        self.fc_b = fc_b
        self.in_v = in_v
        self.out_v = out_v
        self.btn.when_pressed = self.normal_shutdown
        self.shutdown_success = False
        self.threads = []
    
    def set_threads(self, *args):
        for th in args:
            if isinstance(th, LoopingThread):
                self.threads.append(th)

    def normal_shutdown(self):
        """
        SHUTDOWN PROCEDURE:
        1. Envoi signal END to both fuel cells, wait for response
        2. Close H2 inlet valve
        3. Shutdown battery (contactor)
        """
        try:
            self.fc_a.shutdown_fuel_cell()
            self.fc_b.shutdown_fuel_cell()
            self.in_v.close_valve()
            self.out_v.close_valve()
            self.shutdown_success = True
        except Exception:
            raise ShutDownError()
        self.stop_threads()

    def purge_h2(self):
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
        try:
            self.in_v.close_valve()
            self.out_v.open_valve()
            self.he_v.open_valve()
            self.fc_a.purge()
            self.fc_b.purge()
            self.fc_a.shutdown_fuel_cell()
            self.fc_b.shutdown_fuel_cell()
            self.out_v.close_valve()
            self.shutdown_success = True

        except Exception:
            pass
        self.stop_threads()
    
    def stop_threads(self):
        for th in self.threads:
            if isinstance(th, LoopingThread):
                th.stop()
            th.join()

if __name__ == "__main__":
    from ..config import CONFIG
    fc_a = FuelCell(None, None, None, CONFIG['FUELCELL_A'])
    fc_b = FuelCell(None, None, None, CONFIG['FUELCELL_B'])
    BoatStopper(10, fc_a, fc_b, None, None, None).normal_shutdown()