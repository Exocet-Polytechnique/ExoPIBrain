import threading
from asserts.checks import get_check
import serial
from serial.serialutil import SerialTimeoutException
from utils import stringify_data
from asserts.asserts import WarningError, CriticalError
from multithreading.thread import ExoBrainThread
class Consumer(ExoBrainThread):
    """
    This class is a base class for consumers. Consumers are threads that consume data from a queue.
    """
    def __init__(self,lock, queue):
        self.lock = lock
        self.queue = queue

    def run(self):
        pass

class DataConsumer(Consumer):
    """
    The DataConsumer class consumes data from the queue and does the appropriate checks on it during each iteration.
    """
    def __init__(self,lock, queue, gui):
        super().__init__(lock, queue)
        self.gui = gui

    def run(self):
        while not self.st:
            name, data = self.queue.get()[1]
            try:
                get_check(name)(data)
            except Exception as e:
                if isinstance(e, CriticalError):
                   self.gui.dispatch_alert("alert")
                   raise e  # This will cause emergency shutdown
                elif isinstance(e, WarningError):
                    self.gui.dispatch_alert("warning")
            else:
                print(e)
                print(data)
            self.queue.task_done()
           

class LogConsumer(Consumer):
    """
    The LogConsumer class consumes data from the queue and displays it on the screen / 
    writes to IOT cloud by sending it to the MKR1500.
    """
    def __init__(self,lock, log_queue, gui, serial_port):
        super().__init__(lock, log_queue)
        self.serial_port = serial_port
        self.gui = gui
        #self.serial = serial.Serial(self.serial_port, timeout=1, write_timeout=10)
    def efficiency_report(self, data):
        pass

    def write_telemetry(self, name, data):
        """
        This method writes the telemetry data to the MKR1500.
        name (str): The name of the telemetry data.
        data (dict): The value of the telemetry data.
        """
        data_str = stringify_data(name, data)
        data_str = data_str.encode('utf-8')
        #self.serial.write(data_str)

    def write_screen(self, data):
        # TODO: GIVE THE DATA WITH THE CORRECT FORMAT TO THE GUI
        self.gui.update(data)

    def run(self):
        while True:
            try:
                name, data = self.queue.get()
                self.write_telemetry(name, data)
                self.write_screen(data)
                self.queue.task_done()
            except SerialTimeoutException:
                print("Writing timeout. You may want to check the connection.")
            

