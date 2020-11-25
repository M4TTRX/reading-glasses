import cv2
from lib.ocr.tesseract_ocr import OCR
from lib.speech.text_to_speech import TextToSpeech


def test_pc():
    ocr = OCR(tesseract_path="C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
    tts = TextToSpeech()

    img = cv2.imread("lib/ocr/test_images/PXL_20201117_200200158.jpg")
    text = ocr.get_text(img)
    print(text)
    tts.say(text)
    return


def test():
    ocr = OCR()
    img = cv2.imread("lib/ocr/test_images/PXL_20201117_200200158.jpg")
    text = ocr.get_text(img)


if __name__ == "__main__":
    test_pc()
