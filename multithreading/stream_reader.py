import threading
import time

class StreamReader(threading.Thread):
    def __init__(self, thread_id, lock, read_interval, with_checks):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.lock = lock
        self.read_interval = read_interval
        self.with_checks = with_checks

    def read_raw_data(self):
        return 0

    def alert(self, *args, **kwargs):
        raise NotImplementedError()

    def read(self):
        data = self.read_raw_data()
        if self.with_checks:
            self.alert(data)
        return data

    def run(self):
        while True:
            if self.lock:
                self.lock.acquire()
            data = self.read()
            print(data)
            if self.lock:
                self.lock.release()
            time.sleep(self.read_interval)