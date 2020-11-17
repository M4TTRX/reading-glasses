import cv2
from lib.ocr.tesseract_ocr import OCR
from lib.speech.text_to_speech import TextToSpeech


def test():
    ocr = OCR()
    tts = TextToSpeech()
    img = cv2.imread("lib/ocr/test_images/PXL_20201117_200200158.jpg")
    text = ocr.get_text(img)
    print(text)
    tts.say(text)


if __name__ == "__main__":
    test()
