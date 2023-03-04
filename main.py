from sensors.gps import GPS
import smbus
from sensors.imu.hmc5883l import QMC5883l
from sensors.rpmonitor import RPCPUTemperature
import threading

if __name__ == "__main__":
    lock=threading.Lock()
    # TODO: Start procedure



    # TODO: Sensor/telemetry loop (multithreaded)
    # https://stackoverflow.com/questions/25155267/how-to-send-a-signal-to-the-main-thread-in-python-without-using-join
    # https://stackoverflow.com/questions/25904537/how-do-i-send-data-to-a-running-python-thread
    gps = GPS(0, lock, 5, True)
    cputemp = RPCPUTemperature(1, lock, 3, True)

    cputemp.start()
    gps.start()
    

    # TODO: Shutdown sequence
    cputemp.join()
    
    
