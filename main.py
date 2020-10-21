from lib.speech.text_to_speech import TextToSpeech
from lib.camera.img_provider import ImageProvider
import os


def main():
    path = os.path.abspath(os.getcwd())
    print(path)
    img_provider = ImageProvider(path=f"{path}/captured/img.jpg")
    img_provider.getImg()


if __name__ == "__main__":
    main()