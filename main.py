from sensors.gps import GPS
import smbus
from sensors.imu.hmc5883l import QMC5883l
from time import sleep
from sensors.rpmonitor import RPCPUTemperature
import threading

if __name__ == "__main__":
    lock=threading.Lock()
    # TODO: Start procedure



    # TODO: Sensor/telemetry loop (multithreaded)
    cputemp = RPCPUTemperature(1, lock, 0.2, True)
    cputemp.start()

    

    # TODO: Shutdown sequence
    cputemp.join()
    
    
