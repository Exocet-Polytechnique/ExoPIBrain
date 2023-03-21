import serial
from serial.serialutil import SerialException
from multithreading.stream_reader import StreamReader
from gpiozero import CPUTemperature


READ_INTERVAL = 5

class RPCPUTemperature(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config) -> None:
        super().__init__(config['priority'], lock, data_queue, log_queue, config['read_interval'])
        self.monitor = CPUTemperature()

    def read_raw_data(self):
        return "CPU_t", self.monitor.temperature