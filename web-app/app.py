from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from pymongo import MongoClient

app = Flask(__name__)
socketio = SocketIO(app)


# mongoDB client set up
mongo_client = MongoClient('mongodb://localhost:27017/') 
db = mongo_client['people_counter']  # database name for the number of people 
collection = db['images']  # collection where all the images will be stored 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture_image():
    image_data = request.data  # the images come as raw data 
    # plugging in the image data on mongoDB
    result = collection.insert_one({'image': image_data})
    return jsonify({"message": "Image captured and saved", "id": str(result.inserted_id)})

# socketIO set up
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
