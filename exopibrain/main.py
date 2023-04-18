from sensors.gps import GPS
from sensors.rpmonitor import RPCPUTemperature
from fuel_cell.fuel_cell import FuelCell
import threading
from queue import PriorityQueue, Queue
from multithreading.consumers import DataConsumer, LogConsumer
from config import CONFIG

#arduino_serial = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

data_queue = PriorityQueue(maxsize=100)
log_queue = Queue(maxsize=100)
lock=threading.Lock()

if __name__ == "__main__":
    # TODO: Start procedure
    
    # TODO: Sensor/telemetry loop (multithreaded)
    # https://stackoverflow.com/questions/25155267/how-to-send-a-signal-to-the-main-thread-in-python-without-using-join
    # https://stackoverflow.com/questions/25904537/how-do-i-send-data-to-a-running-python-thread

    # Start the fuel cells - must include a start procedure before getting data!
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
    fc_a = FuelCell(lock, data_queue, log_queue, CONFIG["FUELCELL_A"])  # Some random serial ports for now
    fc_b = FuelCell(lock, data_queue, log_queue, CONFIG["FUELCELL_B"])
    fc_a.start_fuel_cell()
    fc_b.start_fuel_cell()

    # Thermocouple

    # Start the sensors
    cputemp = RPCPUTemperature(lock, data_queue, log_queue, CONFIG["RP_CPU_TEMP"])

    #gps = GPS(lock, data_queue, log_queue, CONFIG["GPS"])


    # Start the consumers
    data_cons = DataConsumer(lock, data_queue)  
    log_cons = LogConsumer(lock, log_queue, "/dev/ttyAMA0") # Random port form now

    # Threads
    fc_a.start()
    fc_b.start()
    cputemp.start()
    #gps.start()
    data_cons.start()
    log_cons.start()
    

    # TODO: Shutdown sequence
    """
    SHUTDOWN PROCEDURE:
    1. Envoi signal END to both fuel cells, wait for response
    2. Close H2 inlet valve
    3. Shutdown battery (contactor)
    """
    fc_a.shutdown_fuel_cell()
    fc_b.shutdown_fuel_cell()

    fc_a.join()
    fc_b.join()
    cputemp.join()
    #gps.join()
    data_cons.join()
    
    
