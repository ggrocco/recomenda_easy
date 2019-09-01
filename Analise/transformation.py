import os
import hashlib
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.environ.get('MONGODB_URI')
client = MongoClient(uri)

database = client.get_database()
db = client['heroku_l5cst43x']
comments = db['comments']

for comment in comments.find({}):
  print(comment)

  md5 = 'invalid'
  if comment['AVALIADOR_ID'] != 'ANONIMO':
    md5 = hashlib.md5(comment['AVALIADOR_ID'].encode('utf-8')).hexdigest()

  comments.update_one({"_id": comment['_id']}, {"$set": {"USER_ID": md5}})

