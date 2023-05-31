from sensors.gps import GPS
from sensors.temperature import Thermocouple
from sensors.rpmonitor import RPCPUTemperature
from fuel_cell.fuel_cell import FuelCell
import threading
from queue import PriorityQueue, Queue
from multithreading.consumers import DataConsumer, LogConsumer
from config import CONFIG
from display.ui import GUI
from procedures.shutdown import BoatStopper
from procedures.start import BoatStarter


def main():
    data_queue = PriorityQueue(maxsize=100)
    log_queue = Queue(maxsize=100)
    lock = threading.Lock()
    
    gui = GUI()

    fc_a = FuelCell(lock, data_queue, log_queue, CONFIG["FUELCELL_A"])  # Some random serial ports for now
    fc_b = FuelCell(lock, data_queue, log_queue, CONFIG["FUELCELL_B"])

    # Thermocouple
    #batt_temp = Thermocouple(lock, data_queue, log_queue, CONFIG["BATT_TEMP"])
    # Sensors
    cputemp = RPCPUTemperature(lock, data_queue, log_queue, CONFIG["RP_CPU_TEMP"])
    gps = GPS(lock, data_queue, log_queue, CONFIG["GPS"])

    # Build the consumers
    data_cons = DataConsumer(lock, data_queue, gui)
    log_cons = LogConsumer(lock, log_queue, gui, "/dev/ttyACM0") # Random port for now

    # Threads
    starter = BoatStarter(10, fc_a, fc_b, None, None, None)
    stopper = BoatStopper(10, fc_a, fc_b, None, None, None)
    stopper.set_threads(fc_a, fc_b, cputemp, gps, data_cons, log_cons)

    starter.wait_for_press()
    starter.startup_procedure()

    fc_a.start()
    fc_b.start()
    cputemp.start()
    gps.start()
    data_cons.start()
    log_cons.start()
    print("STARTING GUI...")
    gui.run()


if __name__ == "__main__":
    main()