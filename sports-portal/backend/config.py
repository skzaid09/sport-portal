from pymongo import MongoClient
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sports-portal-secret-key-2025'
    MONGO_URI = "mongodb://localhost:27017/sports_portal"

client = MongoClient(Config.MONGO_URI)
db = client.sports_portal

users = db.users
events = db.events
matches = db.matches