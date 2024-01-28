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

if __name__ == "__main__":
    import time
    actuator1 = Actuator(12)
    actuator2 = Actuator(19)
    while(True):
        print("on allume le 1")
        actuator1.open_valve()
        time.sleep(2)
        print("on allume le 2")
        actuator2.open_valve()
        time.sleep(2)
        print("on ferme le 2")
        actuator2.close_valve()
        time.sleep(2)
        print("on ferme le 1")
        actuator1.close_valve()
        time.sleep(4)
