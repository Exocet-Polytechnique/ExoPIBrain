import serial
from serial.serialutil import SerialException
from multithreading.stream_reader import StreamReader
from gpiozero import CPUTemperature


READ_INTERVAL = 5

class RPCPUTemperature(StreamReader):
    def __init__(self, priority, lock, queue) -> None:
        super().__init__(priority, lock, queue, READ_INTERVAL, True)
        self.monitor = CPUTemperature()

    def read_raw_data(self):
        return "CPU_t", self.monitor.temperature