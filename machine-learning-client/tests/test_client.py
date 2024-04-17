import MLClient
import cv2
class Tests:
    def sanity_check():
        assert True == True, "True does not equal True!"

    def testFaceCounter(self):
        len = facecounter(test.jpg)
        assert isinstance(len, int)
        