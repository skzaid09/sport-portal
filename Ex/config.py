# backend/config.py
import os
from pymongo import MongoClient

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    MONGO_URI = "mongodb://localhost:27017/sports_portal"
    DATABASE_NAME = "sports_portal"

# Initialize MongoDB client
client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]

# Collections
users_collection = db.users
events_collection = db.events
matches_collection = db.matches