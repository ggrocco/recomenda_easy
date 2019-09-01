from flask import Blueprint, request, jsonify
from app import mongo

mod = Blueprint('books_api', __name__)

class BookController():
  @mod.route('/<isbn>')
  def get(isbn):
    book = mongo.db.books.find_one({"ISBN": isbn})
    return jsonify(isbn=book['ISBN'],
                   avg_rank=4)

