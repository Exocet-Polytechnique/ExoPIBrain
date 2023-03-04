from sensors.gps import GPS
import serial
import smbus
from sensors.imu.hmc5883l import QMC5883l
from sensors.rpmonitor import RPCPUTemperature
import threading
from queue import PriorityQueue
from multithreading.consumers import Consumer

#arduino_serial = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

queue = PriorityQueue(maxsize=100)
lock=threading.Lock()

if __name__ == "__main__":
    # TODO: Start procedure
    
    # TODO: Sensor/telemetry loop (multithreaded)
    # https://stackoverflow.com/questions/25155267/how-to-send-a-signal-to-the-main-thread-in-python-without-using-join
    # https://stackoverflow.com/questions/25904537/how-do-i-send-data-to-a-running-python-thread
    gps = RPCPUTemperature(1, lock, queue)#GPS(2, lock, queue)
    cputemp = RPCPUTemperature(1, lock, queue)
    cons = Consumer(lock, queue)

    cputemp.start()
    gps.start()
    cons.start()
    

    # TODO: Shutdown sequence
    cputemp.join()
    gps.join()
    cons.join()
    
    
