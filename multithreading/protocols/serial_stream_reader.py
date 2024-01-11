from multithreading.stream_reader import StreamReader
import serial

class SerialStreamReader(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config):
        """
        This class is used to read a stream of data from a serial port and put it in a queue

        Args:
            lock (threading.Lock): The lock used to synchronize access to the queue.
            data_queue (queue.PriorityQueue): The queue to put the data in.
            log_queue (queue.Queue): The queue to put the data in.
            config (dict): The configuration for the sensor (serial port).
        """
        super().__init__(lock, data_queue, log_queue, config)
        self.ser = serial.Serial(**config['serial'])
    
    def join(self):
        """
        Join the thread and close the serial port.
        """
        super().join()
        self.ser.close()