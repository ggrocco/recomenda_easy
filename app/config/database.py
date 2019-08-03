import os
import pymongo

from flask_pymongo import PyMongo

class MyDB:
  def __init__(self, app):
    mongo = PyMongo(app)




class DB(object):
  URI = os.environ.get('MONGODB_URI')

  @staticmethod
  def init():
    client = PyMongo(app)
    DB.DATABASE = client['sample_app']

  @staticmethod
  def insert(collection, data):
    DB.DATABASE[collection].insert(data)

  @staticmethod
  def find_one(collection, query):
    return DB.DATABASE[collection].find_one(query)
