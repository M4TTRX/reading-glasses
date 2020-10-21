from picamera import PiCamera
from time import sleep
import numpy as np

IMG_WIDTH = 2592
IMG_HEIGHT = 1944
DEFAULT_FRAMERATE = 24


class ImageProvider:
    def __init__(
        self,
        path,
        sleep_timer=5,
        resolution=(IMG_HEIGHT, IMG_WIDTH),
    ):
        self.camera = PiCamera()
        self.sleep_timer = sleep_timer
        self.path = path
        sleep(sleep_timer)

    def getImg(self):
        # self.camera.start_preview()
        # sleep(self.sleep_timer)
        self.camera.capture(self.path)
        # self.camera.stop_preview()