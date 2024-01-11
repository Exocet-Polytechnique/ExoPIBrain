from multithreading.thread import LoopingThread
from sensors.sensor_error import *
import time

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

        # connection status
        self.is_connected = False
    
    def read(self):
        """
        Reads the data from the sensor with name

        Returns:
            tuple: The name of the sensor and the data from the sensor.
        """
        return self.config["name"], self.read_raw_data()

    def run(self):
        """
        Reads the data from the sensor (if connected) and puts it in the queue.
        """
        while not self.stopped():
            if not self.is_connected:
                self.is_connected = self.try_connect()
                continue

            try:
                data = self.read()

                if self.lock:
                    self.lock.acquire()
                self.data_queue.put((self.priority, data))
                self.log_queue.put(data)
                if self.lock:
                    self.lock.release()
            except SensorConnectionError:
                self.is_connected = False
            except InvalidDataError:
                pass

            time.sleep(self.read_interval)

    def read_raw_data(self):
        # Should be overriden by child class
        return 0

    def try_connect(self):
        # To be overriden by child class which need some form of connection with the
        # sensor. Returns True by default (always connected)
        return True