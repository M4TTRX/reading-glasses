from pytesseract import pytesseract, get_tesseract_version, image_to_string
import time


class OCR:
    def __init__(
        self,
        custom_config=r"--oem 3 --psm 6",
        tesseract_path="",
        verbose=False,
    ):
        self.custom_config = custom_config
        self.tesseract_path = tesseract_path

        # set up tesseract
        if tesseract_path != "":
            pytesseract.tesseract_cmd = tesseract_path

        if verbose:
            print("Tesseract version:", get_tesseract_version())

        return

    def get_text(self, img, verbose=False):
        start = time.time()

        # extract the text from the image
        text = image_to_string(img)  # config=self.custom_config

        end = time.time()
        if verbose:
            print("Time elapsed:", end - start)

        return text