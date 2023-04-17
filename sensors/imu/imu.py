from adxl345 import ADXL345
from hmc5883l import HMC5883l
from itg3205 import ITG3205
from data_readers.stream_reader import StreamReader



class IMU(StreamReader):
    def __init__(self, priority, lock, data_queue, log_queue, config):
        super().__init__(priority, lock, data_queue, log_queue, config)
        self.bus = None  # TODO
        self.accelerometer = ADXL345(self.bus)
        self.magnetometer = HMC5883l(self.bus)
        self.gyroscope = ITG3205(self.bus)

    def read_raw_data(self):
        imu_data = {}
        x_acc, y_acc, z_acc = self.accelerometer.read()
        x_mag, y_mag, z_mag = self.magnetometer.read()
        x_gyro, y_gyro, z_gyro = self.gyroscope.read()
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

