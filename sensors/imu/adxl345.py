# ADXL345 Python library for Raspberry Pi
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
#
# This is a Raspberry Pi Python implementation to help you get started with
# the Adafruit Triple Axis ADXL345 breakout board:
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

from sensors.imu.imu_sensor import IMUSensor

class ADXL345(IMUSensor):
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

    def __init__(self, bus):
        super().__init__(bus, address=0x53)

    def connect(self, bus):
        # no need to add this to __init__ since the stream_reader class has its is_connected member to False
        # by default and will attempt to connect via the imu class
        try:
            self.write_byte(self.BW_RATE, self.BW_RATE_100HZ)
            self.set_range(self.RANGE_2G)
            self.write_byte(self.POWER_CTL, self.MEASURE)
        except:
            # failed to connect
            return False

        return True

    def set_range(self, range_flag):
        value = self.bus.read_byte_data(self.address, self.DATA_FORMAT)
        value &= ~0x0F
        value |= range_flag
        value |= 0x08
        self.write_byte(self.DATA_FORMAT, value)

    def read(self, gforce=False):
        """
        returns the current reading from the sensor for each axis

        parameter gforce:
           False (default): result is returned in m/s^2
           True     : result is returned in gs
        """
        i2c_bytes = self.bus.read_i2c_block_data(self.address, self.AXES_DATA, 6)

        x = i2c_bytes[0] | (i2c_bytes[1] << 8)
        if x & (1 << 16 - 1):
            x = x - (1 << 16)

        y = i2c_bytes[2] | (i2c_bytes[3] << 8)
        if y & (1 << 16 - 1):
            y = y - (1 << 16)

        z = i2c_bytes[4] | (i2c_bytes[5] << 8)
        if z & (1 << 16 - 1):
            z = z - (1 << 16)

        x = x * self.SCALE_MULTIPLIER
        y = y * self.SCALE_MULTIPLIER
        z = z * self.SCALE_MULTIPLIER

        if gforce == False:
            x = x * self.EARTH_GRAVITY_MS2
            y = y * self.EARTH_GRAVITY_MS2
            z = z * self.EARTH_GRAVITY_MS2

        return x, y, z
