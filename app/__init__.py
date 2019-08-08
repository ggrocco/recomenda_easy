import os
from flask import Flask
from flask.json import JSONEncoder
from bson import json_util
from flask_pymongo import PyMongo

mongo = PyMongo()

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
      return json_util.default(obj)

# internal
from app.controllers.home_controller import mod as home
from app.controllers.book_controller import mod as books
from app.controllers.api.book_controller import mod as books_api

def create_app():
  app = Flask(__name__,
              static_folder='./static',
              template_folder="./templates")
  app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY'),
    MONGO_URI = os.environ.get('MONGODB_URI')
  )
  app.json_encoder = CustomJSONEncoder

  app.register_blueprint(home)
  app.register_blueprint(books, url_prefix='/books')
  app.register_blueprint(books_api, url_prefix='/api/books')

  mongo.init_app(app)

  return app
