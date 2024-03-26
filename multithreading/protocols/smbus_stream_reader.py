from config import SMBUS_ID
from multithreading.stream_reader import StreamReader
import threading
import smbus2
import time


class SMBusStreamReader(StreamReader):
    WRITE_DELAY_S = 0.01

    _bus_lock = threading.Lock()
    _bus = None

    def __init__(self, lock, data_queue, log_queue, config):
        """
        This class is used to read a stream of data from an SMBus/I2C connection and put it in a queue

        Args:
            lock (threading.Lock): The lock used to synchronize access to the queue.
            data_queue (queue.PriorityQueue): The queue to put the data in.
            log_queue (queue.Queue): The queue to put the data in.
            config (dict): The configuration for the sensor (I2C device id).
        """
        super().__init__(lock, data_queue, log_queue, config)

        if SMBusStreamReader._bus is None:
            SMBusStreamReader._bus = smbus2.SMBus(SMBUS_ID)
        
        self.address = config["i2c_address"]
        self.__has_lock = False

    def acquire_bus_lock(self):
        try:
            self.lock.acquire()
            self.__has_lock = True
            yield None
        finally:
            self.lock.release()
            self.__has_lock = False

    def write_byte(self, register, value):
        if not self.__has_lock:
            print("SMBusStreamReader: lock not acquired before using bus")

        SMBusStreamReader._bus.write_byte_data(self.address, register, value)
        time.sleep(self.WRITE_DELAY_S)

    def read_byte(self, register):
        if not self.__has_lock:
            print("SMBusStreamReader: lock not acquired before using bus")

        return SMBusStreamReader._bus.read_byte_data(self.address, register)

    def read_block(self, register, length):
        if not self.__has_lock:
            print("SMBusStreamReader: lock not acquired before using bus")

        return SMBusStreamReader._bus.read_i2c_block_data(self.address, register, length)
