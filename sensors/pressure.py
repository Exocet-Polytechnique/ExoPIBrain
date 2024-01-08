from multithreading.stream_reader import StreamReader

class Manometer(StreamReader):
    """
    Manometer class used to read pressure data from H2 supplies.
    Compatible with S-model Swagelok PTI transducers: 
    https://www.swagelok.com/downloads/webcatalogs/en/ms-02-225.pdf
    """
    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)
        