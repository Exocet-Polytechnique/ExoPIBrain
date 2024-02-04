from multithreading.protocols.digital_stream_reader import DigitalStreamReader
import RPi.GPIO as GPIO

class StartButton(DigitalStreamReader):
    """
    Class to read the start of the start/stop button
    """

    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)

    def read_raw_data(self):
        return GPIO.input(self._pins[0])

if __name__ == "__main__":
    import time
    from config import CONFIG
    start_button = StartButton(None, None, None, CONFIG["START_BUTTON"])
    while (True):
        print(start_button.read_raw_data())
        time.sleep(1)