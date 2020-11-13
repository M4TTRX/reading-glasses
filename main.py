from lib.speech.text_to_speech import TextToSpeech
from lib.camera.img_provider import ImageProvider
from lib.io.button.trigger_button import TriggerButton
from lib.ocr.mock_ocr import MockOCR


def main(
    tts=TextToSpeech(),
    img_provider=ImageProvider(),
    trigger_button=TriggerButton(),
    ocr=MockOCR(),
):
    while True:
        trigger_button.wait_for_trigger()
        img = img_provider.get_img()
        text = ocr.get_text(img)
        tts.say(text)


if __name__ == "__main__":
    main()