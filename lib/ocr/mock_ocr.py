MESSAGE = "The cake is a lie!"


class FakeOCR:
    def __init__(
        self, message=MESSAGE,
    ):
        self.message = message

    def get_text(self, img) -> str:
        return self.message
