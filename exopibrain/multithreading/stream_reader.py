import threading
import time
from multithreading.thread import ExoBrainThread

class StreamReader(ExoBrainThread):
    """
    This class is used to read a stream of data from a sensor and put it in a queue
    on a new thread. The data is read at a specified interval on a new thread.
    It is a data producer.
    """
    def __init__(self, lock, data_queue, log_queue, config):
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
        return self.config["name"], self.read_raw_data()

    def run(self):
        while not self.stopped():
            if self.lock:
                self.lock.acquire()
            data = self.read()
            self.data_queue.put((self.priority, data))
            self.log_queue.put(data)
            if self.lock:
                self.lock.release()
            time.sleep(self.read_interval)