import cv2
import numpy as np
import pytesseract as pt


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
            pt.pytesseract.tesseract_cmd = tesseract_path
        print("Tesseract version:", pt.get_tesseract_version())
        return

    def pre_process(self, img):
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed_img = cv2.threshold(
            processed_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]
        processed_img = self.deskew(processed_img)
        return processed_img

    def deskew(self, image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )
        return rotated

    def get_text(self, img):
        text = pt.image_to_string(img, config=self.custom_config)
        text = text.replace("\n", " ").replace("\r", "")
        return text