from lib.speech.text_to_speech import TextToSpeech
from lib.camera.img_provider import ImageProvider
import os
import cv2


def main():
    path = os.path.abspath(os.getcwd())
    print(path)
    img_provider = ImageProvider(path=f"{path}/captured/img.jpg")
    img = img_provider.getImg()
    cv2.imwrite("coolpic.jpg", img)


if __name__ == "__main__":
    main()