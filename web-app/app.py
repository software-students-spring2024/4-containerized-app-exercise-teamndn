from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient, DESCENDING
import sys

app = Flask(__name__)

#Establishing MongoDB connection.
try:
    mongo_client = MongoClient("mongodb://localhost:27017/")
    db = mongo_client["people_counter_app"]
    visitor_counts = db["people_counts"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}", file=sys.stderr)
    sys.exit(1)  #Exiting the application if cannot connect to database.

@app.route('/')
def home():
    #Home page route that displays the current visitor count. 
    try:
        # Fetch the most recent visitor count from the database
        latest_data = visitor_counts.find_one(sort=[('_id', DESCENDING)])
        current_count = latest_data['count'] if latest_data else 0
        # Debug print to the console.
        print(f"Current count from DB: {current_count}")
    except Exception as e:
        print(f"Error fetching count from MongoDB: {e}", file=sys.stderr)
        current_count = 0  

    return render_template("index.html", visitor_count=current_count)

@app.route('/update-count', methods=['POST'])
def update_count():
    #Route to update the vistor count based on data received in the request.
    data = request.get_json()

    if data and "count" in data:
        try:
            #Insert the new count into the database.
            new_count = data["count"]
            visitor_counts.insert_one({"count": new_count})
            print(f"Inserted new count into DB: {new_count}")  #Debug print.
            return jsonify({"success": True, "message": "Visitor count updated.", "count": new_count}), 200
        except Exception as e:
            print(f"Error inserting count into MongoDB: {e}", file=sys.stderr)
            return jsonify({"success": False, "error": "Failed to update the count."}), 500
    else:
        return jsonify({"success": False, "error": "Invalid request. 'count' not found in payload."}), 400

if __name__ == '__main__':
    app.run(debug=True)  
