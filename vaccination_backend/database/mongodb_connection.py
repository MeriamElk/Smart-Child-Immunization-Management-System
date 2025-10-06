from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["vaccination_db"]
alertes_collection = mongo_db["alertes"]
logs_collection = mongo_db["logs"]
