import cv2
from lib.speech.text_to_speech import TextToSpeech


def main():
    tts = TextToSpeech()
    tts.say("Hello World")


if __name__ == "__main__":
    main()