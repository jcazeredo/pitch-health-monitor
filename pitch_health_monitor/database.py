from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/admin")
client = MongoClient(MONGO_URI)
db = client.get_database()