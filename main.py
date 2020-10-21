from lib.speech.text_to_speech import TextToSpeech
from lib.camera.img_provider import ImageProvider
import os


def main():
    img_provider = ImageProvider(
        path=f"{os.path.abspath(os.getcwd())}+/captured/img.jpg"
    )
    img_provider.getImg()


if __name__ == "__main__":
    main()