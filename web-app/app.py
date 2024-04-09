from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

#SetTING up a connection to the local MongoDB
mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)

#Database and collection.
db = client['people_counter_app']
collection = db['people_counts']

@app.route('/')
def index():
    # Retrieve the latest count from the database.
    latest_count = collection.find_one(sort=[('_id', -1)])
    count = latest_count['count'] if latest_count else 0
    return render_template('index.html', count=count)

@app.route('/update', methods=['POST'])
def update_count():
    if not request.json or 'count' not in request.json:
        return jsonify({'error': 'Bad Request', 'message': 'No count provided.'}), 400

    count = request.json['count']
    collection.insert_one({'count': count})
    return jsonify({'message': 'Count updated successfully!', 'count': count}), 200

if __name__ == '__main__':
    app.run(debug=True)
