from flask_pymongo import MongoClient

mongo_client = MongoClient('mongo')
db = mongo_client['5bytes']
