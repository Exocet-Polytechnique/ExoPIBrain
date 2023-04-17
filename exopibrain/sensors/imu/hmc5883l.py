from sensors.imu.imu_sensor import IMUSensor
import time


class QMC5883l(IMUSensor):
    RANGE_2G = 0x00
    BW_10Hz = 0x00
    OS_512 = 0x00
    MODE_CONT = 0x01
    REG_CONTROL_1 = 0x0B  # Control Register #1.
    REG_CONTROL_2 = 0x0A  # Control Register #2.
    REG_XOUT_LSB = 0x00  # Output Data Registers for magnetic sensor.
    REG_YOUT_LSB = 0x02
    REG_ZOUT_LSB = 0x04
    REG_RST_PERIOD = 0x0b   # SET/RESET Period Register.

    # Flags for Status Register #1.
    STAT_DRDY = 0b00000001  # Data Ready.
    STAT_OVL = 0b00000010  # Overflow flag.
    STAT_DOR = 0b00000100  # Data skipped for reading.

    def __init__(self, bus, declination=0.0):
        super().__init__(bus, address=0x0C)
        self.declination = declination
        self._calibration = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        self.write_byte(self.REG_CONTROL_1, 0x00)
        self.write_byte(self.REG_CONTROL_2, 0x4D)


    def _read_word(self, registry):
        """Read a two bytes value stored as LSB and MSB."""
        low = self.read_byte(registry)
        high = self.read_byte(registry + 1)
        val = (high << 8) + low
        return val

    def _read_word_2c(self, registry):
        """Calculate the 2's complement of a two bytes value."""
        val = self._read_word(registry)
        if val >= 0x8000:  # 32768
            return val - 0x10000  # 65536
        else:
            return val

    def set_calibration(self, value):
        """Set the 3x3 matrix for horizontal (x, y) magnetic vector calibration."""
        c = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        for i in range(0, 3):
            for j in range(0, 3):
                c[i][j] = float(value[i][j])
        self._calibration = c


    def read(self):
        """Read data from magnetic and temperature data registers."""
        x, y, z = None, None, None
        
        x = self._read_word_2c(self.REG_XOUT_LSB)
        y = self._read_word_2c(self.REG_YOUT_LSB)
        z = self._read_word_2c(self.REG_ZOUT_LSB)
        
        return x, y, z
