from pymongo import MongoClient
import os
mongo_uri = os.environ.get("MONGO_URI")

client = MongoClient(mongo_uri)
db = client[os.environ.get("MONGO_DB_NAME", "test-db")]