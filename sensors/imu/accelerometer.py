# ADXL345 Python library for Raspberry Pi
#
# authors:  Jonathan Williamson and Exocet Polymtl
# license: BSD, see LICENSE.txt included in this package
#
# This is a Raspberry Pi Python implementation to help you get started with
# the Adafruit Triple Axis ADXL345 breakout board:
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer
from multithreading.protocols.smbus_stream_reader import SMBusStreamReader
from utils import to_int16


class Accelerometer(SMBusStreamReader):
    # ADXL345 constants
    DATA_FORMAT = 0x31
    BW_RATE = 0x2C
    POWER_CTL = 0x2D
    BW_RATE_100HZ = 0x0B
    MEASURE = 0x08
    RANGE_2G = 0x00
    EARTH_GRAVITY_MS2 = 9.80665
    SCALE_MULTIPLIER = 0.004
    AXES_DATA = 0x32

    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)

    def try_connect(self):
        # no need to add this to __init__ since the stream_reader class has its is_connected member to False
        # by default and will attempt to connect via the imu class
        try:
            with self.acquire_bus_lock():
                self.write_byte(self.BW_RATE, self.BW_RATE_100HZ)
                self._set_range(self.RANGE_2G)
                self.write_byte(self.POWER_CTL, self.MEASURE)

        except:
            # failed to connect
            return False

        return True

    def _set_range(self, range_flag):
        value = self.read_byte(self.DATA_FORMAT)
        value &= ~0x0F
        value |= range_flag
        value |= 0x08
        self.write_byte(self.DATA_FORMAT, value)

    def read_raw_data(self):
        """
        returns the current reading from the sensor for each axis
        """
        with self.acquire_bus_lock():
            i2c_bytes = self.read_block(self.AXES_DATA, 6)

        x = to_int16(i2c_bytes[1], i2c_bytes[0])
        y = to_int16(i2c_bytes[3], i2c_bytes[2])
        z = to_int16(i2c_bytes[5], i2c_bytes[4])

        x *= self.SCALE_MULTIPLIER
        y *= self.SCALE_MULTIPLIER
        z *= self.SCALE_MULTIPLIER

        x *= self.EARTH_GRAVITY_MS2
        y *= self.EARTH_GRAVITY_MS2
        z *= self.EARTH_GRAVITY_MS2

        return x, y, z

if __name__ == "__main__":
    import time
    from config import CONFIG
    accelerometer = Accelerometer(None, None, None, CONFIG["ADXL345"])
    accelerometer.try_connect()
    while True:
        print(accelerometer.read_raw_data())
        time.sleep(CONFIG["ADXL345"]["read_interval"])
