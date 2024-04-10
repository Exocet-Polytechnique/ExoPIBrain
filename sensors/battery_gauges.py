from multithreading.protocols.smbus_stream_reader import SMBusStreamReader
from utils import to_uint16
import RPi.GPIO as GPIO
import time


# battery gauge datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/2944fa.pdf
# I2C multiplexer datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/4312f.pdf 
class BatteryGauges(SMBusStreamReader):
    CONTROL_REGISTER = 0x01

    VOLTAGE_REGISTER = 0x08
    CURRENT_REGISTER = 0x0E
    CHARGE_REGISTER = 0x02

    # ADC mode: sleep, prescaler: 4096 (default), ALCC disabled
    INITIAL_CONFIGUARION = 0b00111000
    REQUEST_ADC_UPDATE = 0b01111000

    GAUGE_SWITCH_DELAY = 0.01

    # switch these if necessary
    GAUGE_24V = GPIO.HIGH
    GAUGE_12V = GPIO.LOW

    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)
        self._select_gpio = config["select_gpio"]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._select_gpio, GPIO.OUT)

    def try_connect(self):
        try:
            with self.acquire_bus_lock():
                # write to the first battery gauge ...
                self._switch_gauge(self.GAUGE_12V)
                self.write_byte(self.CONTROL_REGISTER, self.INITIAL_CONFIGUARION)

                # ... and the second
                self._switch_gauge(self.GAUGE_24V)
                self.write_byte(self.CONTROL_REGISTER, self.INITIAL_CONFIGUARION)

        except:
            return False
        
        return True

    def _switch_gauge(self, gauge):
        GPIO.output(self._select_gpio, gauge)
        time.sleep(self.GAUGE_SWITCH_DELAY)

    def _request_adc_update(self, gauge):
        self._switch_gauge(gauge)
        self.write_byte(self.CONTROL_REGISTER, self.REQUEST_ADC_UPDATE)

    def _read_gauge_values(self, gauge):
        self._switch_gauge(gauge)
        voltage_data = self.read_block(self.VOLTAGE_REGISTER, 2)
        current_data = self.read_block(self.CURRENT_REGISTER, 2)
        charge_data = self.read_block(self.CHARGE_REGISTER, 2)
        voltage = to_uint16(voltage_data[0], voltage_data[1])
        current = to_uint16(current_data[0], current_data[1])
        charge = to_uint16(charge_data[0], charge_data[1])
        return voltage, current, charge

    def read_raw_data(self):
        with self.acquire_bus_lock():
            # request new values from the sensors
            self._request_adc_update(self.GAUGE_12V)
            self._request_adc_update(self.GAUGE_24V)
            # then read the values
            voltage_12V, current_12V, charge_level_12V = self._read_gauge_values(self.GAUGE_12V)
            voltage_24V, current_24V, charge_level_24V = self._read_gauge_values(self.GAUGE_24V)

        return {
            "BATTERY_12V": {
                "voltage": voltage_12V,
                "current": current_12V,
                "charge_level": charge_level_12V,
            },
            "BATTERY_24V": {
                "voltage": voltage_24V,
                "current": current_24V,
                "charge_level": charge_level_24V,
            }
        }
