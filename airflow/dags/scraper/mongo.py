from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
from bson import json_util

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["article_cache"]
collection = db["articles"]

# Load initial data from JSON file to MongoDB
with open("data_research_biochemistry_2019_2019.json") as f:
    data = json.load(f)
    for article in data:
        title = article["Title"]
        collection.update_one({"Title": title}, {"$set": article}, upsert=True)


@app.route("/get_article", methods=["GET"])
def get_article():
    title = request.args.get("title")
    cached_article = collection.find_one({"Title": title})

    if cached_article:
        print(type(cached_article))
        return json.loads(json_util.dumps(cached_article))
    else:
        return jsonify({"message": "Article not found"}), 404


@app.route("/update_article", methods=["POST"])
def update_article():
    try:
        # Get JSON data from request body
        data = request.json

        # Extract title from JSON data
        title = data.get("Title")

        # Check if title exists in JSON data
        if not title:
            return jsonify({"error": "Title is missing in the request body"}), 400

        # Create key-map object for update

        # Update MongoDB document
        result = collection.update_one({"Title": title}, {"$set": data}, upsert=True)
        # Check if document was updated successfully
        if result:
            return jsonify({"message": "Article updated successfully"})
        else:
            return jsonify({"error": "Article not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
def start_mongo():
    app.run(debug=True)


if __name__ == "__main__":
    start_mongo()
