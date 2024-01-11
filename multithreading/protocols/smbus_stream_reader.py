
from multithreading.stream_reader import StreamReader
import smbus

class SMBusStreamReader(StreamReader):
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
        revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]
        self.bus = smbus.SMBus(config["new_rev_i2c_id"] if int(revision, 16) >= 4 else config["old_rev_i2c_id"])