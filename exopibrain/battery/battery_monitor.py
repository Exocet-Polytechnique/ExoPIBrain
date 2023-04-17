from multithreading.stream_reader import StreamReader

class BatteryMonitor(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)