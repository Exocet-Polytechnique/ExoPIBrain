import smbus
from sensors.imu.adxl345 import ADXL345
from sensors.imu.hmc5883l import QMC5883l
from sensors.imu.itg3205 import ITG3205
from multithreading.stream_reader import StreamReader



class IMU(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)
        revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]
        self.bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)
        self.accelerometer = ADXL345(self.bus)
        self.magnetometer = QMC5883l(self.bus)
        self.gyroscope = ITG3205(self.bus)

    def read_raw_data(self):
        imu_data = {}
        x_acc, y_acc, z_acc = self.accelerometer.read()
        x_mag, y_mag, z_mag = self.magnetometer.read()
        x_gyro, y_gyro, z_gyro = self.gyroscope.read()
        imu_data["x_acc"] = "{:04f}".format(x_acc)
        imu_data["y_acc"] = "{:04f}".format(y_acc)
        imu_data["z_acc"] = "{:04f}".format(z_acc)
        imu_data["x_mag"] = x_mag
        imu_data["y_mag"] = y_mag
        imu_data["z_mag"] = z_mag
        imu_data["x_gyro"] = x_gyro
        imu_data["y_gyro"] = y_gyro
        imu_data["z_gyro"] = z_gyro
        return imu_data

if __name__ == "__main__":
    import time
    from config import CONFIG
    imu = IMU(None, None, None, CONFIG['IMU'])
    while True:
        print(imu.read_raw_data())
        time.sleep(1)