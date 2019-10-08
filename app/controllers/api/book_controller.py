from flask import Blueprint, request, jsonify
from app import mongo
from app.services.recomenda_easy import RecomendaEasy
from app.modelo.process_model import ProcessModel

mod = Blueprint('books_api', __name__)

class BookController():
  @mod.route('/<isbn>')
  def get(isbn):
    book = mongo.db.books.find_one({'$where': f"/{isbn}/.test(this.isbn)"})
    if book is None:
      return jsonify(error='book not found.'), 404

    return jsonify(book=book), 200

  @mod.route('/<user_id>/recomendacao')
  def recomendacao(user_id):
    books = mongo.db.books.find(
        {}, {'_id': 0, 'book_id': 1, 'isbn': 1, 'average_rating': 1, 'ratings_count': 1})
    recomendacoes = RecomendaEasy.recomenda(books, user_id)
    return jsonify(recomendacoes=recomendacoes.to_dict('records')), 200

  @mod.route('/processes_module', methods=['PUT'])
  def processes_module():
    ProcessModel.build_model()
    return jsonify(msg='done.'), 200
