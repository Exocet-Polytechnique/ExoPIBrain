from multithreading.protocols.smbus_stream_reader import SMBusStreamReader


class Compass(SMBusStreamReader):
    # HMC5883L constants
    RANGE_2G = 0x00
    BW_10Hz = 0x00
    OS_512 = 0x00
    MODE_CONT = 0x01
    REG_CONTROL_1 = 0x0B  # Control Register #1.
    REG_CONTROL_2 = 0x0A  # Control Register #2.
    REG_XOUT_LSB = 0x00  # Output Data Registers for magnetic sensor.
    REG_YOUT_LSB = 0x02
    REG_ZOUT_LSB = 0x04
    REG_RST_PERIOD = 0x0B   # SET/RESET Period Register.

    # Flags for Status Register #1.
    STAT_DRDY = 0b00000001  # Data Ready.
    STAT_OVL = 0b00000010  # Overflow flag.
    STAT_DOR = 0b00000100  # Data skipped for reading.

    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)

    def try_connect(self):
        # no need to add this to __init__ since the stream_reader class has its is_connected member to False
        # by default and will attempt to connect via the imu class
        try:
            with self.acquire_lock():
                self.write_byte(self.REG_CONTROL_1, 0x00)
                self.write_byte(self.REG_CONTROL_2, 0x4D)

        except:
            return False

        return True


    def _read_word(self, register):
        """Read a two bytes value stored as LSB and MSB."""
        low = self.read_byte(register)
        high = self.read_byte(register + 1)

        val = (high << 8) + low
        return val

    def _read_word_2c(self, register):
        """Calculate the 2's complement of a two bytes value."""
        val = self._read_word(register)
        if val >= 0x8000:  # 32768
            return val - 0x10000  # 65536
        else:
            return val

    def read_raw_data(self):
        """Read data from magnetic and temperature data registers."""
        with self.acquire_lock():
            x = self._read_word_2c(self.REG_XOUT_LSB)
            y = self._read_word_2c(self.REG_YOUT_LSB)
            z = self._read_word_2c(self.REG_ZOUT_LSB)
        
        return x, y, z

if __name__ == "__main__":
    import time
    from config import CONFIG
    compass = Compass(None, None, None, CONFIG["HMC5883L"])
    compass.try_connect()
    while True:
        print(compass.read_raw_data())
        time.sleep(CONFIG["HMC5883L"]["read_interval"])
