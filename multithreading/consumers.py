import threading
from asserts.checks import get_check
import serial

class Consumer(threading.Thread):
    def __init__(self,lock, queue):
        threading.Thread.__init__(self)
        self.lock = lock
        self.queue = queue
    
    def run(self):
        pass
class DataConsumer(Consumer):
    def __init__(self,lock, queue, serial_port):
        super().__init__(lock, queue)
        

    def run(self):
        while True:
            name, data = self.queue.get()[1]
            get_check(name)(data)
            print(data)
            self.queue.task_done()

class LogConsumer(Consumer):
    def __init__(self,lock, log_queue, serial_port):
        super().__init__(lock, log_queue)
        self.serial_port = serial_port
        self.serial = serial.Serial(self.serial_port)

    def write_telemetry(self, data):
        pass

    def write_screen(self, data):
        pass

    def run(self):
        # TODO: Emit to the arduino and display on the screen
        data = self.queue.get()
        self.write_telemetry(data)
        self.write_screen(data)
        self.queue.task_done()

