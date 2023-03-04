import threading
from asserts.checks import get_check

class Consumer(threading.Thread):
    def __init__(self,lock, queue):
        threading.Thread.__init__(self)
        self.lock = lock
        self.queue = queue
    
    def run(self):
        while True:
            name, data = self.queue.get()[1]
            get_check(name)(data)
            print(data)
            self.queue.task_done()
