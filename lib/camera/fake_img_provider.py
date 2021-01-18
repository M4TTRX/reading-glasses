import cv2


class MockImageProvider:
    def get_img(self, sleep_timer=1, verbose=False, save_image=False):

        return cv2.imread("lib/camera/fake_img/PXL_20201117_200200158.jpg")
