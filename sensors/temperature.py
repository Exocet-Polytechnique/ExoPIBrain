import os
import time
import glob
from multithreading.stream_reader import StreamReader


# From: https://randomnerdtutorials.com/raspberry-pi-ds18b20-python/
class Thermocouple(StreamReader):
    """
    Reads temperature data from the DS18B20 thermocouple
    """
    def __init__(self, lock, data_queue, log_queue, config):
        super(Thermocouple, self).__init__(lock, data_queue, log_queue, config)

        # Thermocouple data wire should be linked to GPIO4 (see boot/config.txt, last line)
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def _read_lines(self):
        """
        Reads the lines from the thermocouple file.

        Returns:
            list: The lines from the thermocouple file.
        """
        with open(self.device_file, 'r') as f:
            lines = f.readlines()
        return lines

    def read_raw_data(self):
        """
        Reads the raw data from the thermocouple with
        correct formatting.

        Returns:
            float: The raw temperature data from the thermocouple.
        """
        temp_c = None
        lines = self._read_lines()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_lines()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
        return temp_c

if __name__ == "__main__":
    import time
    from config import CONFIG
    thermocouple = Thermocouple(None, None, None, CONFIG["TEMPERATURES"])
    while True:
        print(thermocouple.read_raw_data())
        time.sleep(1)
