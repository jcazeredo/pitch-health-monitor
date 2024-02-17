from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/admin")
client = MongoClient(MONGO_URI, uuidRepresentation='standard')
pitches_collection = client.get_database().get_collection('pitches')