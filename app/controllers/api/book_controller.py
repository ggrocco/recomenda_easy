from flask import Blueprint, request, make_response
from app import mongo

mod = Blueprint('books_api', __name__)

class BookController():
  @mod.route('/<isbn>')
  def get(isbn):
    book = mongo.db.books.find_one({"ISBN": isbn})
    return make_response(book, 200)

