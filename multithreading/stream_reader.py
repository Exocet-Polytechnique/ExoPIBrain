import time
from multithreading.thread import LoopingThread
from sensors.sensor_error import SensorConnectionError, InvalidDataError, SensorException
from procedures.exception_handling.sensor_result import SensorResult
from procedures.exception_handling.messages import create_message_id, ERROR_DISCONNECTED, INFO_CONNECTED, WARNING_BAD_DATA

class StreamReader(LoopingThread):
    """
    This class is used to read a stream of data from a sensor and put it in a queue
    on a new thread. The data is read at a specified interval on a new thread.
    It is a data producer.
    """

    MAX_INVALID_DATA = 3

    def __init__(self, lock, data_queue, log_queue, config):
        super(StreamReader, self).__init__()
        self.config = config
        self.priority = self.config["priority"]
        self.lock = lock
        self.read_interval = self.config["read_interval"]
        self.data_queue = data_queue
        self.log_queue = log_queue

        # connection status
        self.is_connected = False
        self.invalid_data_counter_ = 0

    def read(self):
        """
        Reads the data from the sensor with name

        Returns:
            tuple: The name of the sensor and the data from the sensor.
        """
        return self.config["name"], self.read_raw_data()

    def run(self):
        """
        Reads the data from the sensor (if connected) and puts it in the queue.
        """
        while not self.stopped():
            if not self.is_connected:
                self.is_connected = self.try_connect()
                if self.is_connected:
                    self.data_queue.put((self.priority, SensorResult(
                        False, create_message_id(self.config["name"], INFO_CONNECTED))))

                continue

            try:
                data = self.read()

                if self.invalid_data_counter_ >= self.MAX_INVALID_DATA:
                    raise SensorConnectionError()

                if self.lock:
                    with self.lock:
                        self.data_queue.put((self.priority, SensorResult(True, data)))
                        self.log_queue.put(data)
                else:
                    self.data_queue.put((self.priority, SensorResult(True, data)))
                    self.log_queue.put(data)

                self.invalid_data_counter_ = 0

            except SensorConnectionError:
                self.is_connected = False
                self.data_queue.put((self.priority, SensorResult(
                    False, create_message_id(self.config["name"], ERROR_DISCONNECTED))))
                self.log_queue.put(None)
            except InvalidDataError:
                self.data_queue.put((self.priority, SensorResult(
                    False, create_message_id(self.config["name"], WARNING_BAD_DATA))))
                self.log_queue.put(None)
            except SensorException as e:
                # allows sending custom message ids through
                self.data_queue.put((self.priority, SensorResult(
                    False, create_message_id(self.config["name"], e.exception_id))))
                self.log_queue.put(None)

            time.sleep(self.read_interval)

    def read_raw_data(self):
        # Should be overriden by child class
        return 0

    def try_connect(self):
        # To be overriden by child class which need some form of connection with the
        # sensor. Returns True by default (no connection required in some cases)
        return True
