import time
from multithreading.thread import LoopingThread
import serial

class StreamReader(LoopingThread):
    """
    This class is used to read a stream of data from a sensor and put it in a queue
    on a new thread. The data is read at a specified interval on a new thread.
    It is a data producer.
    """
    def __init__(self, lock, data_queue, log_queue, config):
        super(StreamReader, self).__init__()
        self.config = config
        self.priority = self.config["priority"]
        self.lock = lock
        self.read_interval = self.config["read_interval"]
        self.data_queue = data_queue
        self.log_queue = log_queue

    def read_raw_data(self):
        # Should be overriden by child class
        return 0
    
    def read(self):
        """
        Reads the data from the sensor with name

        Returns:
            tuple: The name of the sensor and the data from the sensor.
        """
        return self.config["name"], self.read_raw_data()

    def run(self):
        """
        Reads the data from the sensor and puts it in the queue.
        """
        while not self.stopped():
            if self.lock:
                self.lock.acquire()
            data = self.read()
            self.data_queue.put((self.priority, data))
            self.log_queue.put(data)
            if self.lock:
                self.lock.release()
            time.sleep(self.read_interval)

class SerialStreamReader(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config):
        """
        This class is used to read a stream of data from a serial port and put it in a queue

        Args:
            lock (threading.Lock): The lock used to synchronize access to the queue.
            data_queue (queue.PriorityQueue): The queue to put the data in.
            log_queue (queue.Queue): The queue to put the data in.
            config (dict): The configuration for the sensor (serial port).
        """
        super().__init__(lock, data_queue, log_queue, config)
        self.ser = serial.Serial(**config['serial'])
    
    def join(self):
        """
        Join the thread and close the serial port.
        """
        super().join()
        self.ser.close()
