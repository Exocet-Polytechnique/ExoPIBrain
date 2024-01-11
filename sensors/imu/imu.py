from sensors.imu.adxl345 import ADXL345
from sensors.imu.hmc5883l import QMC5883
from sensors.imu.itg3205 import ITG3205
from multithreading.protocols.smbus_stream_reader import SMBusStreamReader
from sensors.sensor_error import SensorConnectionError
import smbus



class IMU(SMBusStreamReader):
    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)
        self.accelerometer = ADXL345(self.bus)
        self.magnetometer = QMC5883(self.bus)
        self.gyroscope = ITG3205(self.bus)

    def read_raw_data(self):
        imu_data = {}
        try:
            x_acc, y_acc, z_acc = self.accelerometer.read()
            x_mag, y_mag, z_mag = self.magnetometer.read()
            x_gyro, y_gyro, z_gyro = self.gyroscope.read()
        except:
            raise SensorConnectionError

        imu_data["x_acc"] = x_acc
        imu_data["y_acc"] = y_acc
        imu_data["z_acc"] = z_acc
        imu_data["x_mag"] = x_mag
        imu_data["y_mag"] = y_mag
        imu_data["z_mag"] = z_mag
        imu_data["x_gyro"] = x_gyro
        imu_data["y_gyro"] = y_gyro
        imu_data["z_gyro"] = z_gyro
        return imu_data

    def try_connect(self):
        accelerometer_status = self.accelerometer.connect()
        magnetometer_status = self.magnetometer.connect()
        gyroscope_status = self.gyroscope.connect()
        return accelerometer_status and magnetometer_status and gyroscope_status

if __name__ == "__main__":
    import time
    from config import CONFIG
    imu = IMU(None, None, None, CONFIG['IMU'])
    imu.try_connect()
    while True:
        print(imu.read_raw_data())
        time.sleep(1)