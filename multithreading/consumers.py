from asserts.checks import perform_check
from multithreading.thread import LoopingThread
from serial.serialutil import SerialTimeoutException
from utils import stringify_data
import serial
from procedures.exception_handling.messages import get_message_severity, CRITICAL_ERROR


class Consumer(LoopingThread):
    """
    This class is a base class for consumers. Consumers are threads that consume data from a queue.
    """

    def __init__(self, lock, queue):
        super(Consumer, self).__init__()
        self.lock = lock
        self.queue = queue

    def run(self):
        pass


class DataConsumer(Consumer):
    """
    The DataConsumer class consumes data from the queue and does the appropriate checks on it during each iteration.
    """

    def __init__(self, lock, queue, gui):
        super().__init__(lock, queue)
        self.gui = gui
        # TODO when we implement procedures
        self.shutdown_procedure = None

    def requires_shutdown(self, message_id):
        """
        Determines if the message is severe enough to trigger the shutdown procedure.
        """
        return get_message_severity(message_id) <= CRITICAL_ERROR

    def process_exception(self, sensor_result):
        """
        Processes the result of the sensor data by showing sending a message to the gui and
        starting the shutdown procedure if necessary. The result must be an exception.
        """
        self.gui.dispatch_message(sensor_result.get_error_message_id())
        if self.requires_shutdown(sensor_result.get_error_message_id()):
            self.shutdown_procedure.start()

    def run(self):
        """
        Reads the data from the queue and does the appropriate checks on it.

        Raises:
            CriticalError: If the data is critical.
            WarningError: If the data is a warning.
        """
        while not self.stopped():
            self.lock.acquire()
            name, data = self.queue.get()
            self.lock.release()

            if data.is_valid():
                check_results = perform_check(name, data.value)
                if isinstance(check_results, list):
                    for result in check_results:
                        if not result.is_valid():
                            self.process_exception(result)
                elif not check_results.is_valid():
                    self.process_exception(check_results)

            else:
                self.process_exception(data)

            self.queue.task_done()


class LogConsumer(Consumer):
    """
    The LogConsumer class consumes data from the queue and displays it on the screen /
    writes to IOT cloud by sending it to the MKR1500.
    """

    def __init__(self, lock, log_queue, gui, serial_port):
        super().__init__(lock, log_queue)
        self.serial_port = serial_port
        self.gui = gui
        self.serial = serial.Serial(self.serial_port, timeout=1, write_timeout=10)

    def efficiency_report(self, data):
        pass

    def write_telemetry(self, name, data):
        """
        This method writes the telemetry data to the MKR1500.
        name (str): The name of the telemetry data.
        data (dict): The value of the telemetry data.
        """
        data_str = stringify_data(name, data)
        data_str = data_str.encode("utf-8")
        self.serial.write(data_str)

    def write_screen(self, data):
        self.gui.update(data)

    def run(self):
        """
        Reads the data from the queue and writes it to the MKR1500 and the screen.
        """
        while not self.stopped():
            try:
                self.lock.acquire()
                name, data = self.queue.get()
                self.lock.release()
                self.write_telemetry(name, data)
                self.write_screen(data)
                self.queue.task_done()
            except SerialTimeoutException:
                print("Writing timeout. You may want to check the connection.")
