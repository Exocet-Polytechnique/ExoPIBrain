from multithreading.protocols.smbus_stream_reader import SMBusStreamReader
from utils import to_int16


class Gyroscope(SMBusStreamReader):
    """
    https://github.com/ControlEverythingCommunity/ITG3200/blob/master/Python/ITG_3200.py
    """
    # ITG3205 constants
    POWER_MANAGEMENT = 0x3E
    PLL_X_GYRO = 0x01
    DLPF_FS = 0x16
    DLPF_256_8 = 0x18
    DATA_REG = 0x1D

    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)

    def try_connect(self):
        try:
            with self.acquire_bus_lock():
                self.write_byte(self.POWER_MANAGEMENT, self.PLL_X_GYRO)
                self.write_byte(self.DLPF_FS, self.DLPF_256_8)

        except:
            return False

        return True

    def read_raw_data(self):
        with self.acquire_bus_lock():
            data = self.read_block(self.DATA_REG, 6)

        # Convert the data
        x = to_int16(data[0], data[1])
        y = to_int16(data[2], data[3])
        z = to_int16(data[4], data[5])
        return x, y, z


if __name__ == "__main__":
    import time
    from config import CONFIG
    gyroscope = Gyroscope(None, None, None, CONFIG["ITG3205"])
    gyroscope.try_connect()
    while True:
        print(gyroscope.read_raw_data())
        time.sleep(CONFIG["ITG3205"]["read_interval"])
