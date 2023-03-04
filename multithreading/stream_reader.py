import threading
import time

class StreamReader(threading.Thread):
    def __init__(self, priority, lock, queue, read_interval, with_checks):
        threading.Thread.__init__(self)
        self.priority = priority
        self.lock = lock
        self.read_interval = read_interval
        self.with_checks = with_checks
        self.queue = queue

    def read_raw_data(self):
        return "None", 0


    def run(self):
        while True:
            if self.lock:
                self.lock.acquire()
            data = self.read_raw_data()
            self.queue.put((self.priority, data))
            print("in queue", data)
            if self.lock:
                self.lock.release()
            time.sleep(self.read_interval)