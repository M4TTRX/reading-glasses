import sys, getopt

# Import Mocks
from lib.speech.fake_text_to_speech import MockTextToSpeech
from lib.ocr.mock_ocr import MockOCR
from lib.camera.fake_img_provider import MockImageProvider
from lib.io.button.pc_button import PCTriggerButton
from lib.preprocessing.paper_crop import get_lines_from_img


def start(
    tts,
    img_provider,
    trigger_button,
    ocr,
):
    from lib.preprocessing.paper_crop import get_lines_from_img

    while True:
        # Wait for the user to press the button
        trigger_button.wait_for_trigger()

        img = []
        # Capture the image
        try:
            img = img_provider.get_img(save_image=True, verbose=True)
        except:
            message = "Could not capture the image"
            print(f"⚠ {message}")
            tts.say(message)
            pass
        img_lines = get_lines_from_img(img, display_img=True)
        # Break down the image into paragraph for more performant processing
        if len(img_lines) > 0:
            for line in img_lines:
                text = ocr.get_text(line)
                print(text)
                tts.say(text)
            tts.say("\n\nOver")
        else:
            tts.say("Error, no paper was detected")


def get_ocr(arg=""):
    print("Intializing OCR...", end="\t\t")
    if arg == "real" or arg == "r":
        print("Real", end=" ")
        try:
            from lib.ocr.tesseract_ocr import OCR

            ocr = OCR()
        except:
            print("❌")
            return
    else:
        print("Fake", end=" ")
        ocr = MockOCR()
    print("✅")
    return ocr


def get_tts(arg=""):
    print("Intializing TTS...", end="\t\t")
    if arg == "real" or arg == "r":
        print("Real", end=" ")
        try:
            from lib.speech.text_to_speech import TextToSpeech

            tts = TextToSpeech()
        except:
            print("❌")
            return
    else:
        print("Fake", end=" ")
        tts = MockTextToSpeech()
    print("✅")
    return tts


def get_img_provider(arg=""):
    print("Intializing Image Provider...", end="\t")
    if arg == "real" or arg == "r":
        print("Real", end=" ")
        try:
            from lib.camera.img_provider import ImageProvider

            img_provider = ImageProvider()
        except:
            print("❌")
            return
    else:
        print("Fake", end=" ")
        img_provider = MockImageProvider()
    print("✅")
    return img_provider


def get_trigger_button(arg=""):
    print("Intializing Trigger Button...", end="\t")
    if arg == "real" or arg == "r" or arg == "physical":
        print("Real", end=" ")
        try:
            from lib.io.button.trigger_button import TriggerButton

            trigger_button = TriggerButton()
        except:
            print("❌")
            return
    else:
        print("Fake", end=" ")
        trigger_button = PCTriggerButton()
    print("✅")
    return trigger_button


def main(argv):
    tts_arg = ""
    img_provider_arg = ""
    trigger_button_arg = ""
    ocr_arg = ""
    try:
        opts, args = getopt.getopt(
            argv,
            "p:o:s:i:b:",
            ["preset=", "ocr=", "tts=", "img_prov=", "trigger_button="],
        )
    except getopt.GetoptError:
        help_msg = (
            "Please use the proper arguments:\n"
            "--------------------------------\n"
            "-p, --preset\t Uses one preset f\nor options.\n"
            "-o\n"
        )
        print()

    # Apply presets first
    for opt, arg in opts:
        if opt in ("-p", "--preset"):
            # The pi_real preset runs everything as it should in the final
            # product
            if arg == "pi_real":
                tts_arg = "r"
                img_provider_arg = "r"
                trigger_button_arg = "r"
                ocr_arg = "r"

            # The pc preset runs everything using real components except for
            # the camera and the image provider
            elif arg == "pc":
                tts_arg = "r"
                ocr_arg = "r"

    # Apply individual options then
    for opt, arg in opts:
        if opt in ("-o", "--ocr"):
            ocr_arg = arg
        elif opt in ("-s", "--tts"):
            tts_arg = arg
        elif opt in ("-i", "--img_prov"):
            img_provider_arg = arg
        elif opt in ("-b", "--trigger_button"):
            trigger_button_arg = arg

    tts = get_tts(tts_arg)
    img_provider = get_img_provider(img_provider_arg)
    trigger_button = get_trigger_button(trigger_button_arg)
    ocr = get_ocr(ocr_arg)
    start(
        tts,
        img_provider,
        trigger_button,
        ocr,
    )


if __name__ == "__main__":
    main(sys.argv[1:])