from multithreading.stream_reader import StreamReader
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class Manometer(StreamReader):
    """
    Manometer class used to read pressure data from H2 supplies.
    Compatible with S-model Swagelok PTI transducers: 
    https://www.swagelok.com/downloads/webcatalogs/en/ms-02-225.pdf
    """
    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.D25)
        self.mcp = MCP.MCP3008(self.spi, self.cs)
        self.channels = [AnalogIn(self.mcp, MCP.P0)]

    def _convert_to_pressure(self, channel_value):
        # TODO
        return channel_value

    def read_raw_data(self):
        return self._convert_to_pressure(self.channels[0].value)

if __name__ == "__main__":
    import time
    from config import CONFIG
    manometer = Manometer(None, None, None, CONFIG["MANOMETERS"])
    while (True):
        print(manometer.read_raw_data())
        time.sleep(1)