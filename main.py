from lib.speech.text_to_speech import TextToSpeech
from lib.camera.img_provider import ImageProvider


def main():
    path = os.path.abspath(os.getcwd())
    img_provider = ImageProvider(path=f"{path}/captured/img.jpg")
    img_arr = img_provider.getImg()
    im = Image.fromarray(img_arr)
    im.save("test.png")


if __name__ == "__main__":
    main()