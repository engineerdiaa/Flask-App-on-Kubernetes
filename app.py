from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
import json

app = Flask(__name__)

# MongoDB Configuration
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongodb-service')
MONGO_PORT = 27017
USERNAME = 'admin'
PASSWORD = 'admin'

# Initialize Connection
client = MongoClient(f"mongodb://{USERNAME}:{PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/")
db = client.bookstore_db
books_collection = db.books

# Seed our Data (populate the database)
@app.route('/init-db', methods=['POST'])
def init_db():
    # Script to avoid redundancy
    if books_collection.count_documents({}) == 0:
        try:
            with open('bookstore.json', 'r') as file:
                data = json.load(file)
                books_collection.insert_many(data)
            return jsonify({"message": "Database initialized with bookstore.json"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"message": "Database already contains data"}), 200

# CRUD Below

# 1. Get a book (read)
@app.route('/books', methods=['GET'])
def get_books():
    books = list(books_collection.find({}, {'_id': 0}))
    return jsonify(books), 200

# 2. Add a new book (create)
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    books_collection.insert_one(data)
    return jsonify({"message": "Book added successfully"}), 201

# 3. UPDATE (ISBN PK)
@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    data = request.json
    result = books_collection.update_one({'isbn': isbn}, {'$set': data})
    if result.matched_count:
        return jsonify({"message": "Book updated"}), 200
    return jsonify({"error": "Book not found"}), 404

# 4. DELETE (ISBN PK too)
@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    result = books_collection.delete_one({'isbn': isbn})
    if result.deleted_count:
        return jsonify({"message": "Book deleted"}), 200 # status code for success
    return jsonify({"error": "Book not found"}), 404 # status code for not found

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # Starts the app
                                       # 0.0.0.0 important for kubernetes communication.