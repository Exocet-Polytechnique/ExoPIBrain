from multithreading.stream_reader import StreamReader
from gpiozero import CPUTemperature

class RPCPUTemperature(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config) -> None:
        super().__init__(lock, data_queue, log_queue, config)
        self.monitor = CPUTemperature()

    def read_raw_data(self):
        return {"temperature": self.monitor.temperature}