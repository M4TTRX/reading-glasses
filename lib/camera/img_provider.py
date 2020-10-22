from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep

IMG_WIDTH = 2592
IMG_HEIGHT = 1944
DEFAULT_FRAMERATE = 24


class ImageProvider:
    def __init__(
        self,
        path,
        sleep_timer=2,
        resolution=(IMG_HEIGHT, IMG_WIDTH),
    ):
        self.camera = PiCamera()
        self.sleep_timer = sleep_timer
        self.path = path
        sleep(sleep_timer)

    def getImg(self):
        # self.camera.capture(self.path)

        # grab a reference to the raw cam capture
        rawCapture = PiRGBArray(self.camera)

        # allow the camera to warmup
        sleep(self.sleep_timer)

        self.camera.capture(rawCapture, format="rgb")
        return rawCapture.array
