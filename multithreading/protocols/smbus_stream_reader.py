from config import SMBUS_NEW_ID, SMBUS_OLD_ID
from multithreading.stream_reader import StreamReader
import threading
import smbus2


class SMBusStreamReader(StreamReader):
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
            revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]
            SMBusStreamReader._bus = smbus2.SMBus(SMBUS_NEW_ID if int(revision, 16) >= 4 else SMBUS_OLD_ID)
