import threading
from queue import Queue
import time

queueLock = threading.Lock()
workQueue = Queue(100)


class Processor(threading.Thread):
    def __init__(self, thread_id, q):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.q = q

    def run(self):
        while True:
            queueLock.acquire()
            if not workQueue.empty():
                obj = self.q.get()
                data = obj.read()
                print(data)
            else:
                queueLock.release()
            time.sleep(1)
