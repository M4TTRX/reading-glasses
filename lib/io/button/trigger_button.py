from time import sleep
import RPi.GPIO as GPIO


class IOButtonError(Exception):
    """Exception raised for errors happening with the trigger button."""

    pass


class TriggerButton:
    def __init__(
        self,
        button_pin=17,
        sleep_timer=0.1,
    ):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def wait_for_trigger(self, verbose=False):
        try:
            while GPIO.input(self.buttonPin):
                sleep(self.sleep_timer)
            if verbose:
                print("Button Trigger Detected")
        except:
            GPIO.cleanup()
            raise IOButtonError()
        GPIO.cleanup()
