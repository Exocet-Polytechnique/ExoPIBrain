from multithreading.stream_reader import StreamReader
import RPi.GPIO as GPIO

class DigitalStreamReader(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config):
        """
        This class is used to read input from a GPIO pin

        Args:
            lock (threading.Lock): The lock used to synchronize access to the queue.
            data_queue (queue.PriorityQueue): The queue to put the data in.
            log_queue (queue.Queue): The queue to put the data in.
            config (dict): The configuration containing the pin to use.
        """
        super().__init__(lock, data_queue, log_queue, config)
        GPIO.setmode(GPIO.BCM)
        self._pin = config["pin"]
        GPIO.setup(self._pin, GPIO.IN)

    def join(self):
        """
        Join the thread and cleanup used pin
        """
        super().join()
        GPIO.cleanup(self._pins)
