from pymongo import MongoClient

# pprint library is used to make the output look more pretty
import datetime
from pprint import pprint

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
uri = "<< MONGODB URL >>"

client = MongoClient(uri)

print("Connection Successful")
# client.close() 
db = client['<< MONGODB DATABASE >>']
pprint(db.list_collection_names())
books = db['books']
# pprint(books.find({}))

for x in books.find({},{"ISBN":1,"_id":0}):
  pprint(x) 
