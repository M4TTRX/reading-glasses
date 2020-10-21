from picamera import PiCamera
from time import sleep
import numpy as np

IMG_WIDTH = 2592
IMG_HEIGHT = 1944
DEFAULT_FRAMERATE = 24


class ImageProvider:
    def __init__(
        self,
        sleep_timer=5,
        resolution=(IMG_HEIGHT, IMG_WIDTH),
    ):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = DEFAULT_FRAMERATE
        self.sleep_timer = sleep_timer
        sleep(sleep_timer)

    def getImg(self):
        # self.camera.start_preview()
        # sleep(self.sleep_timer)
        self.camera.capture("captured_img/img.jpg")
        # self.camera.stop_preview()