from multithreading.stream_reader import StreamReader
import RPi.GPIO as GPIO

class DigitalStreamReader(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config):
        """
        This class is used to read input from one (or more) digital GPIO pins

        Args:
            lock (threading.Lock): The lock used to synchronize access to the queue.
            data_queue (queue.PriorityQueue): The queue to put the data in.
            log_queue (queue.Queue): The queue to put the data in.
            config (dict): The configuration for the sensor (I2C device id).
        """
        super().__init__(lock, data_queue, log_queue, config)
        GPIO.setmode(GPIO.BCM)
        if "pin" in config:
            self._pins = [config["pin"]]
        elif "pins" in config:
            self._pins = config["pins"]
        else:
            raise ValueError("No pin or pins specified in the configuration.")

        # the library allows setting multiple pins at once by passing in a list
        GPIO.setup(self._pins, GPIO.IN)

    def join(self):
        """
        Join the thread and cleanup used pins
        """
        super().join()
        GPIO.cleanup(self._pins)
