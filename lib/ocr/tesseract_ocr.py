from cv2 import cvtColor, threshold, COLOR_BGR2GRAY, THRESH_BINARY, THRESH_OTSU
from pytesseract import pytesseract, get_tesseract_version, image_to_string
from .helpers import resize_img, deskew
import time


class OCR:
    def __init__(
        self,
        custom_config=r"--oem 3 --psm 6",
        tesseract_path="",
    ):
        self.custom_config = custom_config
        self.tesseract_path = tesseract_path

        # set up tesseract
        if tesseract_path != "":
            pytesseract.tesseract_cmd = tesseract_path
        print("Tesseract version:", get_tesseract_version())
        return

    def pre_process(self, img):
        processed_img = cvtColor(img, COLOR_BGR2GRAY)
        processed_img = resize_img(processed_img)
        processed_img = threshold(processed_img, 0, 255, THRESH_BINARY + THRESH_OTSU)[1]
        processed_img = deskew(processed_img)
        return processed_img

    def get_text(self, img, verbose=True):
        start = time.time()

        # pre process the image
        img = self.pre_process(img)

        # extract the text from the image
        text = image_to_string(img)  # config=self.custom_config

        # remove newline characters,
        # which will improve the text to speech down the line
        text = text.replace("\n", " ").replace("\r", "")

        end = time.time()
        if verbose:
            print("Time elapsed:", end - start)

        return text