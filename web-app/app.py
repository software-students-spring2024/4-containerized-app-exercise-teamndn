from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from pymongo import MongoClient
import base64, os

app = Flask(__name__)
socketio = SocketIO(app)

# mongoDB client set up
mongo_client = MongoClient('mongodb://mongodb:27017/')
db = mongo_client['start']
unprocessed_images = db['unprocessed_images']  # collection for unprocessed images
processed_data = db['processed_data']  # collection for processed results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture_image():
    # extracting image data from the POST request
    image_data = request.get_data().decode('utf-8').split(',')[1]  
    image_bytes = base64.b64decode(image_data)
    
    # saving the image data to the 'unprocessed_images' collection
    result = unprocessed_images.insert_one({'image': image_bytes})
    return jsonify({"message": "Image captured and saved", "id": str(result.inserted_id)})

@app.route('/results')
def results():
    # fetching all entries from the 'processed_data' collection
    results = list(unprocessed_images.find({}, {'_id': 0}))
    print(results)
    return render_template('results.html', results=results)

# socketIO set up
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
