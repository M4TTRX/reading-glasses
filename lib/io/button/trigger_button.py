from time import sleep
import RPi.GPIO as GPIO


class IOButtonError(Exception):
    """Exception raised for errors happening with the trigger button."""

    pass


def button_callback(channel):
    print("Button was pushed!")


class TriggerButton:
    def __init__(
        self,
        button_pin=11,  # GPIO 17
        sleep_timer=0.1,
    ):
        self.button_pin = button_pin
        self.sleep_timer = sleep_timer
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def wait_for_trigger(self, verbose=False):
        while True:  # Run forever
            if GPIO.input(self.button_pin) == GPIO.HIGH:
                while GPIO.input(self.button_pin) == GPIO.HIGH:
                    sleep(0.1)
                print("Button was pushed!")
                break


def test():
    btn = TriggerButton()
    btn.wait_for_trigger(verbose=True)


if __name__ == "__main__":
    test()