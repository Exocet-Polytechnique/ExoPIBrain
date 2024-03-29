import RPi.GPIO as GPIO
from config import BUTTON_DEBOUNCE_S
import time

class StartButton:
    """
    Class to read the state of the start/stop button
    """

    def __init__(self, config):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config["pin"], GPIO.IN)

        # Start at high to prevent the boat from automatically starting if the button is
        # already pressed when the boat is turned on
        self._last_state = True
        self._pin = config["pin"]

    def was_pressed(self):
        """
        Check if the button was just pressed.

        This will return True only if the button was not pressed the last time its state was checked and is
        now pressed.
        """
        state = bool(GPIO.input(self._pin))
        if state != self._last_state:
            # software debounce:
            time.sleep(BUTTON_DEBOUNCE_S)
            self._last_state = state
            return state

        return False

if __name__ == "__main__":
    from config import CONFIG
    start_button = StartButton(CONFIG["START_BUTTON"])
    while (True):
        print(start_button.was_pressed())
        time.sleep(0.5)
