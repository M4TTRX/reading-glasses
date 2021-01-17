import cv2
from lib.ocr.tesseract_ocr import OCR
from lib.preprocessing.paper_crop import get_lines_from_img


def test_pc():
    from lib.speech.text_to_speech import TextToSpeech

    ocr = OCR(tesseract_path="C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
    tts = TextToSpeech()

    img = cv2.imread("lib/ocr/test_images/PXL_20201117_200200158.jpg")
    # img = cv2.imread("lib/camera/img_saves/5.jpg")
    lines = get_lines_from_img(img, display_img=True)
    for line in lines:
        text = ocr.get_text(line)
        print(text)
        tts.say(text)
    return


def test():
    ocr = OCR()
    img = cv2.imread("lib/camera/img_saves/5.jpg")
    lines = get_lines_from_img(img)
    for line in lines:
        text = ocr.get_text(line)
        print(text)


if __name__ == "__main__":
    test_pc()
