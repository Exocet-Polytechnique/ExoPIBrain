import threading
import time

class StreamReader(threading.Thread):
    def __init__(self, priority, lock, data_queue, log_queue, read_interval):
        threading.Thread.__init__(self)
        self.priority = priority
        self.lock = lock
        self.read_interval = read_interval
        self.data_queue = data_queue
        self.log_queue = log_queue

    def read_raw_data(self):
        return "None", 0


    def run(self):
        while True:
            if self.lock:
                self.lock.acquire()
            data = self.read_raw_data()
            self.data_queue.put((self.priority, data))
            self.log_queue.put(data)
            print("in queue", data)
            if self.lock:
                self.lock.release()
            time.sleep(self.read_interval)