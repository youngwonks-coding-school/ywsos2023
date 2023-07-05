from pymongo import MongoClient
import os
mongo_uri = os.environ.get('MONGO_URI')

client = MongoClient(mongo_uri)
db = client['test-db']  # Replace 'your_database_name' with your actual database name