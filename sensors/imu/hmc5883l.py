from sensors.imu.imu_sensor import IMUSensor
import time


class QMC5883l(IMUSensor):
    RANGE_2G = 0x00
    BW_10Hz = 0x00
    OS_512 = 0x00
    MODE_CONT = 0x01
    REG_CONTROL_1 = 0x09  # Control Register #1.
    REG_CONTROL_2 = 0x0A  # Control Register #2.
    REG_XOUT_LSB = 0x00  # Output Data Registers for magnetic sensor.
    REG_XOUT_MSB = 0x01
    REG_YOUT_LSB = 0x02
    REG_YOUT_MSB = 0x03
    REG_ZOUT_LSB = 0x04
    REG_ZOUT_MSB = 0x05
    SOFT_RST = 0b10000000  # Soft Reset.
    INT_ENB = 0b00000001  # Interrupt Pin Enabling.
    REG_STATUS_1 = 0x06  # Status Register.
    REG_RST_PERIOD = 0x0b   # SET/RESET Period Register.

    # Flags for Status Register #1.
    STAT_DRDY = 0b00000001  # Data Ready.
    STAT_OVL = 0b00000010  # Overflow flag.
    STAT_DOR = 0b00000100  # Data skipped for reading.

    def __init__(self, bus, declination=0.0):
        super().__init__(bus, address=0x0C)
        self.declination = declination
        self._calibration = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        self.write_byte(self.REG_CONTROL_2, self.SOFT_RST)
        self.write_byte(self.REG_CONTROL_2, self.INT_ENB)
        self.write_byte(self.REG_RST_PERIOD, 0x01)
        self.write_byte(self.REG_CONTROL_1, self.MODE_CONT)
        chip_id = self.read_byte(0x0d)
        if chip_id != 0xff:
            print(chip_id)


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


    def get_data(self):
        """Read data from magnetic and temperature data registers."""
        i = 0
        [x, y, z] = [None, None, None]
        while i < 20:  # Timeout after about 0.20 seconds.
            status = self.read_byte(self.REG_STATUS_1)
            print(status)
            if status & 0b00000010:   # Overflow flag.
                print("overflow!!")
            if status & self.STAT_DOR:
                # Previous measure was read partially, sensor in Data Lock.
                x = self._read_word_2c(self.REG_XOUT_LSB)
                y = self._read_word_2c(self.REG_YOUT_LSB)
                z = self._read_word_2c(self.REG_ZOUT_LSB)
                continue
            if status & self.STAT_DRDY:
                # Data is ready to read.
                x = self._read_word_2c(self.REG_XOUT_LSB)
                y = self._read_word_2c(self.REG_YOUT_LSB)
                z = self._read_word_2c(self.REG_ZOUT_LSB)
                break
            else:
                # Waiting for DRDY.
                time.sleep(0.01)
                i += 1
        return [x, y, z]
