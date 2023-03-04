import serial
from serial.serialutil import SerialException
from multithreading.stream_reader import StreamReader
from gpiozero import CPUTemperature
from asserts.asserts import AlertError, CriticalError

class RPCPUTemperature(StreamReader):
    def __init__(self, thread_id, lock, read_interval, with_checks=True) -> None:
        super().__init__(thread_id, lock, read_interval, with_checks)
        self.monitor = CPUTemperature()
        self.MAX_TEMP_WARN = 80
        self.MAX_TEMP_ALERT = 90

    def read_raw_data(self):
        return self.monitor.temperature

    def alert(self, temperature):
        msg = f"CPUTemp: {temperature}"
        if self.MAX_TEMP_WARN <= temperature < self.MAX_TEMP_ALERT:
            raise AlertError(msg)
        if temperature > self.MAX_TEMP_ALERT:
            raise CriticalError(msg)