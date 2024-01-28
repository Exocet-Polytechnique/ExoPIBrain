"""
Controls the valve's actuator
"""
import RPi.GPIO as GPIO # works in the raspberrypi


class Actuator():
    def __init__(self, pinNumber):
        GPIO.setmode(GPIO.BCM)
        self.pinNumber = pinNumber
        GPIO.setup(self.pinNumber, GPIO.OUT) # puts the pin pinNumber as an Output
    
    def open_valve(self):
        GPIO.output(self.pinNumber, GPIO.HIGH) #puts a 0 in the pin, witch open the valve

    
    def close_valve(self):
        GPIO.output(self.pinNumber, GPIO.LOW) # puts a 1 in the pin, witch close the valve
