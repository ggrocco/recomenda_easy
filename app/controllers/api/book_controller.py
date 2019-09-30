from flask import Blueprint, request, jsonify
from app import mongo

mod = Blueprint('books_api', __name__)

class BookController():
  @mod.route('/<isbn>')
  def get(isbn):
    book = mongo.db.books.find_one({"isbn": isbn})
    return jsonify(isbn=book['isbn'], avg_rank=4)

