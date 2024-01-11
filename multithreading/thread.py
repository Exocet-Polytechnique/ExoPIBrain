import abc
import threading



class LoopingThread(threading.Thread):
    """
    A simple abstraction over a thread that can be stopped
    with thread events. Useful for threads that use an infinite loop like consumers
    and StreamReaders.
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

    def stop(self):
        """
        Sends a stop signal to the thread.
        """
        self._stop.set()

    def stopped(self):
        """
        Returns:
            bool: True if the thread is stopped, False otherwise.
        """
        return self._stop.isSet()
