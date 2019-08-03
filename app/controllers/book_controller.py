from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter
from app import mongo

mod = Blueprint('books', __name__)

PAGA_SIZE = 50

class BookController():

  @mod.route('/')
  def get():
    current_page = request.args.get(get_page_parameter(), default=1, type=int)
    first_record = PAGA_SIZE*(current_page-1)

    all_books = mongo.db.books.find().skip(first_record).limit(PAGA_SIZE)
    pagination = Pagination(page=current_page, total=all_books.count(
    ), per_page=PAGA_SIZE, record_name='books')
    return render_template('books/index.html', books=all_books, pagination = pagination)

