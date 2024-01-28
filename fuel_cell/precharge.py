"""
"""
import RPi.GPIO as GPIO # works in the raspberrypi
import time

class Precharge():
    """
    The precharge procedure is yet to
    be implemented once we recieve and install the 
    appropriate components.    
    """
    #commentaire : au démarage / GPIO22, GPIO27 / après 2s / GPIO22 GPIO17
    def __init__(self, config):
        GPIO.setmode(GPIO.BCM)

        self.contacteur1 = config["contacteur1"]
        GPIO.setup(self.contacteur1, GPIO.OUT)
        GPIO.output(self.contacteur1, GPIO.LOW)

        self.contacteur2 = config["contacteur2"]
        GPIO.setup(self.contacteur2, GPIO.OUT)
        GPIO.output(self.contacteur2, GPIO.LOW)

        self.contacteur3 = config["contacteur3"]
        GPIO.setup(self.contacteur3, GPIO.OUT)
        GPIO.output(self.contacteur3, GPIO.LOW)
        
    def charge(self):
        GPIO.output(self.contacteur1, GPIO.HIGH)
        GPIO.output(self.contacteur2, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.contacteur2, GPIO.LOW)
        GPIO.output(self.contacteur3, GPIO.HIGH)

    def decharge(self):
        # TODO find a way to discharge the capacitor
        pass
