import threading

class ExoBrainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

def stop(self):
    self._stop.set()

def stopped(self):
    return self._stop.isSet()
