from adxl345 import ADXL345

class IMU:
    def __init__(self) -> None:
        self.accelerometer = ADXL345()
        self.temperature = None
        self.gyroscope = None

    def read_accelerometer(self):
        axes = self.accelerometer.get_axes()
        return axes['x'], axes['y'], axes['z']

    def read_gyroscope(self):
        pass

    def read_temperature(self):
        pass

    
