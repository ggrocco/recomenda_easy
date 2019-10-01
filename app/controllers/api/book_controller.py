from flask import Blueprint, request, jsonify
from app import mongo

mod = Blueprint('books_api', __name__)

class BookController():
  @mod.route('/<isbn>')
  def get(isbn):
    book = mongo.db.books.find_one({'$where': f"/{isbn}/.test(this.isbn)"})
    if book is None:
      return jsonify(error='book not found.'), 404

    return jsonify(book=book), 200

