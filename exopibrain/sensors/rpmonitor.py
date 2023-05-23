from multithreading.stream_reader import StreamReader
from gpiozero import CPUTemperature

class RPCPUTemperature(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config) -> None:
        """
        RP temperature monitoring class

        Args:
            lock (threading.Lock): The lock used to synchronize access to the queue.
            data_queue (queue.PriorityQueue): The queue to put the data in.
            log_queue (queue.Queue): The queue to put the data in.
            config (dict): The configuration for the sensor (serial port).
        """
        super().__init__(lock, data_queue, log_queue, config)
        self.monitor = CPUTemperature()

    def read_raw_data(self):
        """
        Reads the raw data from the sensor.

        Returns:
            dict: The raw data from the sensor.
        """
        return {"temperature": self.monitor.temperature}