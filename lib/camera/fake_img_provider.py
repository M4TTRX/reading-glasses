import cv2


class MockImageProvider:
    def get_img(self, sleep_timer=1, verbose=False, save_image=False):
        img = cv2.imread("lib/camera/fake_img/2.jpg")
        return img