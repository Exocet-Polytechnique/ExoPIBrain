import threading
from asserts.checks import get_check
import serial
from serial.serialutil import SerialTimeoutException
from utils import stringify_data

class Consumer(threading.Thread):
    def __init__(self,lock, queue):
        threading.Thread.__init__(self)
        self.lock = lock
        self.queue = queue
    
    def run(self):
        pass

class DataConsumer(Consumer):
    def __init__(self,lock, queue):
        super().__init__(lock, queue)
    
    def run(self):
        while True:
            name, data = self.queue.get()[1]
            get_check(name)(data)
            #print(data)
            self.queue.task_done()
           

class LogConsumer(Consumer):
    def __init__(self,lock, log_queue, serial_port):
        super().__init__(lock, log_queue)
        self.serial_port = serial_port
        self.serial = serial.Serial(self.serial_port, timeout=1, write_timeout=10)

    def write_telemetry(self, name, data):
        data_str = stringify_data(name, data)
        data_str = data_str.encode('utf-8')
        print(f"writing {data_str}")

        self.serial.write(data_str)
        print("wrote")

    def write_screen(self, name, data):
        pass

    def run(self):
        # TODO: Emit to the arduino and display on the screen
        while True:
            try:
                name, data = self.queue.get()
                self.write_telemetry(name, data)
                self.write_screen(name, data)
                self.queue.task_done()
            except SerialTimeoutException:
                print("Writing timeout. You may want to check the connection.")
            

