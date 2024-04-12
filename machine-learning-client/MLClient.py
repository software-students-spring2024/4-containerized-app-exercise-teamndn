import cv2, pymongo

def faceCounter(img):
    faceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceClassifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces)


connection = pymongo.MongoClient("mongodb://localhost:27017/")
db = connection['start']
while True:
    pics = db.pictures.find({ "faceCount" : { "$exists" : False } })
    for pic in pics:
        ans = count_faces(pic)
        db.pictures.update_one(
            {"_id": pic["_id"]},
            {"$set": {"faceCount": ans}}  
        )
