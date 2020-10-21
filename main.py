import cv2
from lib.speech.text_to_speech import TextToSpeech
from lib.camera.img_provider import ImageProvider


def main():
    img_provider = ImageProvider()
    img_provider.getImg()


if __name__ == "__main__":
    main()