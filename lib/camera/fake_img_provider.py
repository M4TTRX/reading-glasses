import cv2


class FakeImageProvider:
    def get_img(self, verbose=False, save_image=False):
        img = cv2.imread("lib/camera/fake_img/7.jpg")
        return img
