"""
Controls a valve's actuator
"""

import RPi.GPIO as GPIO


class Actuator:
    def __init__(self, output_pin, error_pin, closed_on_low):
        GPIO.setmode(GPIO.BCM)

        self.output_pin_ = output_pin
        GPIO.setup(self.output_pin_, GPIO.OUT)
        # NOTE: should we always ensure the actuator is in its default
        # position? Does the following line garantee that?
        GPIO.output(self.output_pin_, GPIO.LOW)
        self.error_pin_ = error_pin
        self.closed_on_low_ = closed_on_low
    
    def open_valve(self):
        if self.closed_on_low_:
            GPIO.output(self.output_pin_, GPIO.HIGH)
        else:
            GPIO.output(self.output_pin_, GPIO.LOW)

    def close_valve(self):
        if self.closed_on_low_:
            GPIO.output(self.output_pin_, GPIO.LOW)
        else:
            GPIO.output(self.output_pin_, GPIO.HIGH)

    def get_status(self):
        return bool(GPIO.input(self.error_pin_))

if __name__ == "__main__":
    import time
    from config import CONFIG

    TEST_DELAY_S = 3

    # TODO: make sure the actuator doesn't move right after creating the object
    valve1_config = CONFIG["ACTUATORS"]["valve1"]
    actuator = Actuator(valve1_config["output_pin"], valve1_config["error_pin"],
                        valve1_config["closed_on_low"])
    time.sleep(TEST_DELAY_S)
    while(True):
        actuator.open_valve()
        print(actuator.get_status())
        time.sleep(TEST_DELAY_S)
        print(actuator.get_status())
        actuator.close_valve()
        print(actuator.get_status())
        time.sleep(TEST_DELAY_S)
