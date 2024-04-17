import cv2, pymongo, os, numpy, base64

def faceCounter(img):
    imgArr = cv2.imdecode(numpy.frombuffer(img, numpy.uint8), -1)
    
    # Convert the image to grayscale
    grayImg = cv2.cvtColor(imgArr, cv2.COLOR_BGR2GRAY)
    
    # Load the pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Return the number of faces detected
    return len(faces)


connectionn = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
dbn = os.getenv("MONGO_DB", "start")
connection = pymongo.MongoClient(connectionn)
db = connection[dbn]
while True:
    pics = db.unprocessed_images.find({ "faceCount" : { "$exists" : False } })
    for pic in pics:
        ans = faceCounter(pic['image'])
        db.unprocessed_images.update_one(
            {"_id": pic["_id"]},
            {"$set": {"faceCount": ans}}  
        )
