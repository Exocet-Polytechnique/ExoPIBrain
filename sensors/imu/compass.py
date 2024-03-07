from multithreading.protocols.smbus_stream_reader import SMBusStreamReader
from utils import to_int16


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
            with self.acquire_bus_lock():
                self.write_byte(self.REG_CONTROL_1, 0x00)
                self.write_byte(self.REG_CONTROL_2, 0x4D)

        except:
            return False

        return True

    def read_raw_data(self):
        """
        Read data from each axis of the compass.
        """
        with self.acquire_bus_lock():
            data_x = self.read_block(self.REG_XOUT_LSB, 2)
            data_y = self.read_block(self.REG_YOUT_LSB, 2)
            data_z = self.read_block(self.REG_ZOUT_LSB, 2)

        global_x_heading = to_int16(data_x[1], data_x[0])
        global_y_heading = to_int16(data_y[1], data_y[0])
        global_z_heading = to_int16(data_z[1], data_z[0])
        
        return global_x_heading, global_y_heading, global_z_heading


if __name__ == "__main__":
    import time
    from config import CONFIG
    compass = Compass(None, None, None, CONFIG["HMC5883L"])
    compass.try_connect()
    while True:
        print(compass.read_raw_data())
        time.sleep(CONFIG["HMC5883L"]["read_interval"])
