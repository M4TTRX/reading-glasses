from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import os
from PIL import Image
from cv2 import imwrite, cvtColor, COLOR_RGB2BGR

IMG_HEIGHT = 736 * 3
IMG_WIDTH = 480 * 3
DEFAULT_FRAMERATE = 24


class ImageProvider:
    def __init__(
        self,
        sleep_timer=2,
        resolution=(IMG_HEIGHT, IMG_WIDTH),
    ):
        self.camera = PiCamera()
        self.sleep_timer = sleep_timer
        self.resolution = resolution
        self.camera.resolution = resolution
        sleep(sleep_timer)

    def get_img(self, sleep_timer=1, verbose=False, save_image=False):
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

        # save the image if save_image is enabled
        if save_image:
            from datetime import datetime

            img_name = datetime.now().strftime("%d_%m_%Y") + ".jpg"
            print(f"Saving {img_name}")
            imwrite(img_name, cvtColor(img_arr, COLOR_RGB2BGR))
            sleep(self.sleep_timer)
        return img_arr


def test():
    img_provider = ImageProvider()
    img = img_provider.get_img(save_image=True)


if __name__ == "__main__":
    test()