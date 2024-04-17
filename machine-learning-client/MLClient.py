import cv2, pymongo

def faceCounter(img):
    faceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceClassifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces)


connection = pymongo.MongoClient("mongodb://mongodb:27017/")
db = connection['start']
while True:
    pics = db.unprocessed_images.find({ "faceCount" : { "$exists" : False } })
    for pic in pics:
        ans = faceCounter(pic)
        db.pictures.update_one(
            {"_id": pic["_id"]},
            {"$set": {"faceCount": ans}}  
        )
