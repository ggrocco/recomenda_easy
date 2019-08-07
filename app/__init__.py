import os
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

# internal
from app.controllers.home_controller import mod as home
from app.controllers.book_controller import mod as books

def create_app():
  app = Flask(__name__,
              static_folder='./static',
              template_folder="./templates")
  app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY'),
    MONGO_URI = os.environ.get('MONGODB_URI')
  )

  app.register_blueprint(home)
  app.register_blueprint(books, url_prefix='/books')
  mongo.init_app(app)

  return app
