"""
"""

import RPi.GPIO as GPIO
import time

class Precharge():
    """
    Class containing methods to handle the charge and discharge procedures
    of the contactors.
    """

    CHARGE_DELAY = 2
    STAGE_SWITCH_DELAY = 0.5

    def __init__(self, config):
        # address pins with their gpio number (not physical pin number)
        GPIO.setmode(GPIO.BCM)

        self.main_contactor = config["main_contactor"]
        GPIO.setup(self.main_contactor, GPIO.OUT)
        GPIO.output(self.main_contactor, GPIO.LOW)

        self.stage1_contactor = config["stage1_contactor"]
        GPIO.setup(self.stage1_contactor, GPIO.OUT)
        GPIO.output(self.stage1_contactor, GPIO.LOW)

        self.stage2_contactor = config["stage2_contactor"]
        GPIO.setup(self.stage2_contactor, GPIO.OUT)
        GPIO.output(self.stage2_contactor, GPIO.LOW)
        
    def charge(self):
        GPIO.output(self.main_contactor, GPIO.HIGH)
        GPIO.output(self.stage1_contactor, GPIO.HIGH)
        time.sleep(self.CHARGE_DELAY)
        GPIO.output(self.stage1_contactor, GPIO.LOW)

        time.sleep(self.STAGE_SWITCH_DELAY)
        GPIO.output(self.stage2_contactor, GPIO.HIGH)
        time.sleep(self.CHARGE_DELAY)

        # TODO: do we need to do anything else at the end?

    def discharge(self):
        # TODO: Figure out what needs to be done here.
        pass
