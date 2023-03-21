from sensors.gps import GPS
from sensors.imu import IMU
from sensors.rpmonitor import RPCPUTemperature
from fuel_cell.fuel_cell import FuelCell
import threading
from queue import PriorityQueue, Queue
from multithreading.consumers import DataConsumer, LogConsumer

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
    fc_a = FuelCell(0, lock, data_queue, log_queue, "/dev/ttyS0")  # Some random serial ports for now
    fc_b = FuelCell(0, lock, data_queue, log_queue, "/dev/ttyS0")

    # Start the sensors
    cputemp = RPCPUTemperature(1, lock, data_queue, log_queue, "/dev/ttyS0")

    gps = GPS(2, lock, data_queue, log_queue, "/dev/ttyS0")
    imu = IMU(2, lock, data_queue, log_queue)


    # Start the consumers
    data_cons = DataConsumer(lock, data_queue)
    log_cons = LogConsumer(lock, log_queue, "/dev/ttyS0")

    # Threads
    fc_a.start()
    fc_b.start()
    cputemp.start()
    gps.start()
    data_cons.start()
    log_cons.start()
    

    # TODO: Shutdown sequence
    fc_a.join()
    fc_b.join()
    cputemp.join()
    gps.join()
    data_cons.join()
    
    
