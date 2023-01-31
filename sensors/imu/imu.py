from adxl345 import ADXL345
from hmc5883l import HMC5883l
from itg3205 import ITG3205
from data_readers.stream_reader import StreamReader


class IMU(StreamReader):
    def __init__(self):
        super().__init__()
        self.bus = None  # TODO
        self.accelerometer = ADXL345(self.bus)
        self.magnetometer = HMC5883l(self.bus)
        self.gyroscope = ITG3205(self.bus)

    def read_raw_data(self):
        self.accelerometer.read()
        self.magnetometer.read()
        self.gyroscope.read()

    def alert(self, data):
        pass
