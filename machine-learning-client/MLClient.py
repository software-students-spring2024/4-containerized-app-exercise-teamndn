import cv2, pymongo, os, numpy, base64

def faceCounter(img):
    nparr = numpy.frombuffer(img, numpy.uint8)
    
    # Decode the numpy array as an image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Return the number of detected faces
    return len(faces)


connectionn = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
dbn = os.getenv("MONGO_DB", "start")
connection = pymongo.MongoClient(connectionn)
db = connection[dbn]
while True:
    pics = db.unprocessed_images.find({ "faceCount" : { "$exists" : False } })
    for pic in pics:
        ans = faceCounter(pic['image'])
        db.pictures.update_one(
            {"_id": pic["_id"]},
            {"$set": {"faceCount": ans}}  
        )
