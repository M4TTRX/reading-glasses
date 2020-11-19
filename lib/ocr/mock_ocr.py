MESSAGE = "The cake is a lie!"


class MockOCR:
    def __init__(
        self,
        message=MESSAGE,
    ):
        print("Fake OCR created!")

    def get_text(self, img) -> str:
        return self.message