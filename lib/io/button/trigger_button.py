from time import sleep
import RPi.GPIO as GPIO


class IOButtonError(Exception):
    """Exception raised for errors happening with the trigger button."""

    pass


class TriggerButton:
    def __init__(
        self,
        button_pin=11,
        sleep_timer=0.1,
    ):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def wait_for_trigger(self, verbose=False):
        while True:  # Run forever
            if GPIO.input(10) == GPIO.HIGH:
                print("Button was pushed!")
