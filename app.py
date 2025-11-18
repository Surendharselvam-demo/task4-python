from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
books = [
    {"id": 1, "title": "Atomic Habits", "author": "James Clear"},
    {"id": 2, "title": "The Alchemist", "author": "Paulo Coelho"}
]

# ---- ROUTES ----

# Get all books
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

# Get one book by ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"message": "Book not found"}), 404

# Create a new book
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    new_book = {
        "id": books[-1]["id"] + 1 if books else 1,
        "title": data.get("title"),
        "author": data.get("author")
    }
    books.append(new_book)
    return jsonify(new_book), 201

# Update a book
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    return jsonify(book)

# Delete a book
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
