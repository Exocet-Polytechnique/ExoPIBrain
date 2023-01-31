import math
from imu_sensor import IMUSensor

class HMC5883l(IMUSensor):
    MEASURE = 0x00
    MEASUREMENT = 0x00
    BW_15Hz = 0x70
    SCALE = 0x01
    CONTINUOUS = 0x02

    __scales = {
        0.88: [0, 0.73],
        1.30: [1, 0.92],
        1.90: [2, 1.22],
        2.50: [3, 1.52],
        4.00: [4, 2.27],
        4.70: [5, 2.56],
        5.60: [6, 3.03],
        8.10: [7, 4.35],
    }

    def __init__(self, bus, gauss=1.3, declination=(0, 0)):
        super().__init__(bus, address=0x1E)
        degrees, minutes = declination
        self.declination = degrees + minutes / 60
        (reg, self.__scale) = self.__scales[gauss]
        self.bus.write_byte_data(
            self.address, self.MEASURE, self.BW_15Hz
        )  # 8 Average, 15 Hz, normal measurement
        self.bus.write_byte_data(self.address, self.SCALE, reg << 5)  # Scale
        self.bus.write_byte_data(
            self.address, self.CONTINUOUS, self.MEASUREMENT
        )  # Continuous measurement

    def __twos_complement(self, val, length):
        # Convert twos compliment to integer
        if val & (1 << length - 1):
            val = val - (1 << length)
        return val

    def __convert(self, data, offset):
        val = self.__twos_complement(data[offset] << 8 | data[offset + 1], 16)
        if val == -4096:
            return None
        return round(val * self.__scale, 4)

    def axes(self):
        data = self.bus.read_i2c_block_data(self.address, 0x00)
        # print map(hex, data)
        x = self.__convert(data, 3)
        y = self.__convert(data, 7)
        z = self.__convert(data, 5)
        return (x, y, z)

    def read(self):
        (x, y, _) = self.axes()
        heading_rad = math.atan2(y, x)
        heading_rad += self.declination

        # Correct for reversed heading
        if heading_rad < 0:
            heading_rad += 2 * math.pi

        # Check for wrap and compensate
        elif heading_rad > 2 * math.pi:
            heading_rad -= 2 * math.pi

        # Convert to degrees from radians
        heading_deg = heading_rad * 180 / math.pi
        return heading_deg

    def degrees(self, heading_deg):
        degrees = math.floor(heading_deg)
        minutes = round((heading_deg - degrees) * 60)
        return (degrees, minutes)
