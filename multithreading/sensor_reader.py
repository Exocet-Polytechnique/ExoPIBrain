import threading
import time
import logging


class MessagePrinter(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self._args = args
        self._kwargs = kwargs
        self._lock = kwargs.get("lock", None)

    def run(self):
        for message in self._args:
            logging.info(message)
            time.sleep(self._kwargs.get("delay", 1.0))
