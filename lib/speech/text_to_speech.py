import pyttsx3


class TextToSpeech:
    def __init__(
        self,
    ):
        self.speech_engine = pyttsx3.init()

    def say(self, text, speed=120):
        self.speech_engine.setProperty("rate", speed)
        self.speech_engine.say(text)
        self.speech_engine.runAndWait()


def hard_coded_text_test():
    # instantiate the TextToSpeech
    tts = TextToSpeech()
    test_string = "Hello World"
    tts.say(test_string)
    return


if __name__ == "__main__":
    hard_coded_text_test()
    pass
