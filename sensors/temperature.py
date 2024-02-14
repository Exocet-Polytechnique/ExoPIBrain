from multithreading.stream_reader import StreamReader
import os
import time


# From: https://randomnerdtutorials.com/raspberry-pi-ds18b20-python/
# and: https://stackoverflow.com/questions/72771186/read-multiple-ds18b20-temperature-sensors-faster-using-raspberry-pi
class Thermocouples(StreamReader):
    """
    Reads temperature data from the DS18B20 thermocouples.

    Since all the sensors take roughly 750ms to read and we can only read them sequentially,
    there will be a delay of 750ms * number_of_sensors between each read.
    """

    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)

        self._values = {name: float("nan") for name in config["sensors"].keys()}
        self._names = list(config["sensors"].keys())
        addresses = [config["sensors"][name]["address"] for name in config["sensors"].keys()]
        self._device_files = [f"/sys/bus/w1/devices/28-{address:012x}/w1_slave" for address in addresses]
        self._current_sensor_index = 0

        # Thermocouple data wire should be linked to GPIO4 (see boot/config.txt, last line)
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

    def _read_current_sensor(self):
        """
        Read the temperature data from the current sensor.

        Returns:
            False if the sensor is not connected
            True otherwise
        """
        name = self._names[self._current_sensor_index]
        device_file = self._device_files[self._current_sensor_index]

        if not os.path.isfile(device_file):
            self._current_sensor_index += 1
            print(f"Warning: the temperature sensor \"{name}\" is not connected.")
            return False

        with open(self._device_files[self._current_sensor_index], 'r') as f:
            lines = f.readlines()

        if lines[0].strip()[-3:] != 'YES':
            self._current_sensor_index += 1
            print(f"Warning: invalid data received from \"{name}\" temperature sensor.")
            return True

        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            self._values[name] = float(temp_string) / 1000.0

        self._current_sensor_index += 1
        return True

    def read_raw_data(self):
        """
        Reads the raw data from the thermocouple with correct formatting.

        Returns:
            float: The raw temperature data from the thermocouple.
        """
        read_successful = self._read_current_sensor()
        read_counter = 5 # prevent being stuck in an infinite loop
        while not read_successful and read_counter > 0:
            read_counter -= 1
            read_successful = self._read_current_sensor()

        return self._values

if __name__ == "__main__":
    import time
    from config import CONFIG
    thermocouple = Thermocouples(None, None, None, CONFIG["TEMPERATURES"])
    while True:
        print(thermocouple.read_raw_data())
        time.sleep(CONFIG['BATT_TEMP']['read_interval'])
