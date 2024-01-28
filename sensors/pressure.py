from multithreading.stream_reader import StreamReader
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

possible_channels = [MCP.P0, MCP.P1, MCP.P2, MCP.P3, MCP.P4, MCP.P5]


class Manometers(StreamReader):
    MAX_ANALOG_VALUE = 65535.0
    MIN_ANALOG_VALUE = 0.0

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
        self.sensors = config["sensors"]
        self.channels = []
        for i in range(len(self.sensors)):
            self.channels.append(possible_channels[i])

    def _convert_to_pressure(self, channel_value, min, max):
        ratio = (channel_value - Manometers.MIN_ANALOG_VALUE) / (Manometers.MAX_ANALOG_VALUE - Manometers.MIN_ANALOG_VALUE)
        return min + ratio * (max - min)

    def read_raw_data(self):
        output = {}
        for i, (name, (min, max)) in enumerate(self.sensors.items()):
            output[name] = self._convert_to_pressure(self.channels[i], min, max)

        return output

if __name__ == "__main__":
    import time
    from config import CONFIG
    manometers = Manometers(None, None, None, CONFIG["MANOMETERS"])
    while (True):
        print(manometers.read_raw_data())
        time.sleep(1)