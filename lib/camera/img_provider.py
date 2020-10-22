from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import os
from PIL import Image

IMG_WIDTH = 2592
IMG_HEIGHT = 1944
DEFAULT_FRAMERATE = 24


class ImageProvider:
    def __init__(
        self,
        sleep_timer=2,
        resolution=(IMG_HEIGHT, IMG_WIDTH),
    ):
        self.camera = PiCamera()
        sleep(sleep_timer)

    def getImg(self, sleep_timer=1, verbose=False, save_image=False):
        # self.camera.capture(self.path)
        if verbose:
            print("Initiating camera capture...")
        # grab a reference to the raw cam capture
        rawCapture = PiRGBArray(self.camera)

        # allow the camera to warmup
        sleep(self.sleep_timer)

        # capture the image
        self.camera.capture(rawCapture, format="rgb")
        if verbose:
            print("Image capture completed")

        img_arr = rawCapture.array
        # save the image if needed
        if save_image:
            from datetime import datetime

            img_name = datetime.now().strftime("%d/%m/%Y_%H:%M:%S") + ".png"

            img = Image.fromarray(img_arr)
            img.save(img_name)

        return img_arr
