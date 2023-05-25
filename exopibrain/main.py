from sensors.gps import GPS
from sensors.rpmonitor import RPCPUTemperature
from fuel_cell.fuel_cell import FuelCell
import threading
from queue import PriorityQueue, Queue
from multithreading.consumers import DataConsumer, LogConsumer
from config import CONFIG
from display.ui import GUI
from procedures.shutdown import BoatStopper
from procedures.start import BoatStarter

#arduino_serial = serial.Serial("/dev/ttyACM0", 9600, timeout=1)



def main():
    data_queue = PriorityQueue(maxsize=100)
    log_queue = Queue(maxsize=100)
    lock=threading.Lock()
    
    gui = GUI()

    # Start the fuel cells - must include a start procedure before getting data!

    fc_a = FuelCell(lock, data_queue, log_queue, CONFIG["FUELCELL_A"])  # Some random serial ports for now
    fc_b = FuelCell(lock, data_queue, log_queue, CONFIG["FUELCELL_B"])
    #fc_a.start_fuel_cell()
    #fc_b.start_fuel_cell()

    # Thermocouple

    # Start the sensors
    cputemp = RPCPUTemperature(lock, data_queue, log_queue, CONFIG["RP_CPU_TEMP"])

    gps = GPS(lock, data_queue, log_queue, CONFIG["GPS"])

    # Start the consumers
    data_cons = DataConsumer(lock, data_queue, gui)
    log_cons = LogConsumer(lock, log_queue, gui, "/dev/ttyACM0") # Random port form now

    # Threads
    fc_a.start()
    fc_b.start()
    cputemp.start()
    gps.start()
    data_cons.start()
    log_cons.start()

    #BoatStopper()
    print("STARTING GUI...")
    gui.run()


if __name__ == "__main__":
    main()