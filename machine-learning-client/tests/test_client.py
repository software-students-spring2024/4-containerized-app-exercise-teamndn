import cv2
import pymongo
def faceCounter(img):
        faceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image = cv2.imread(img)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceClassifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return len(faces)

class Tests:
    def sanity_check():
        assert True == True, "True does not equal True!"

    def testFaceCounter(self):
        len = faceCounter("tests/test.jpg")
        assert isinstance(len, int), "expected face counter to return int"
        