from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/admin")
db_client = MongoClient(MONGO_URI, uuidRepresentation='standard')