"""
Main file of the project. This will create all the objects necessary for the boat's systems to work
properly. It will also wait for a button press before starting all the procedures and GUI.
"""

from sensors.gps import GPS
from sensors.temperature import Thermocouple
from sensors.rpmonitor import RPCPUTemperature
from fuel_cell.fuel_cell import FuelCell
import threading
from queue import PriorityQueue, Queue
from multithreading.consumers import DataConsumer, LogConsumer
from config import CONFIG, TELE_CONFIG
from display.ui import GUI
from procedures.shutdown import BoatStopper
from procedures.start import BoatStarter


def main():
    # Setup the PriorityQueues and thread lock
    data_queue = PriorityQueue(maxsize=100)
    log_queue = Queue(maxsize=100)
    lock = threading.Lock()

    # Initialize the GUI. Data is transfered later through the consumers
    gui = GUI()

    # Initialize different objects. This does not trigger any startup/initialisation for these
    # systems at hardware level

    # Hydrogen fuel cells
    fc_a = FuelCell(lock, data_queue, log_queue, CONFIG["FUELCELL_A"])
    fc_b = FuelCell(lock, data_queue, log_queue, CONFIG["FUELCELL_B"])

    # Thermocouple
    batt_temp = Thermocouple(lock, data_queue, log_queue, CONFIG["BATT_TEMP"])
    # Sensors
    cputemp = RPCPUTemperature(lock, data_queue, log_queue, CONFIG["RP_CPU_TEMP"])
    gps = GPS(lock, data_queue, log_queue, CONFIG["GPS"])

    # Build the consumers
    data_cons = DataConsumer(lock, data_queue, gui)
    log_cons = LogConsumer(lock, log_queue, gui, TELE_CONFIG["serial_port"])

    # Threads
    starter = BoatStarter(10, fc_a, fc_b, None, None, None)
    stopper = BoatStopper(10, fc_a, fc_b, None, None)
    stopper.set_threads(fc_a, fc_b, cputemp, gps, data_cons, log_cons)

    # Startup: we wait for a button to be pressed before triggering the startup procedure
    starter.wait_for_press()
    starter.startup_procedure()

    # Start threads for all systems
    fc_a.start()
    fc_b.start()
    cputemp.start()
    gps.start()
    batt_temp.start()
    data_cons.start()
    log_cons.start()

    # Start the GUI. The `run` method contains a loop which will keep the program running
    print("STARTING GUI...")
    gui.run()


if __name__ == "__main__":
    main()
