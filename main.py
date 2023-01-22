from sensors.imu import IMU
import time 
if __name__ == "__main__":
    imu = IMU()
    while True:
        time.sleep(1)
        x,y,z = imu.read_accelerometer()
        print(f"{x}, {y}, {z}")