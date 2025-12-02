# backend/config.py
import os
from pymongo import MongoClient

class Config:
    # Use environment variable in Render, fallback to local for testing
    MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/sports_portal"

client = MongoClient(Config.MONGO_URI)
db = client.sports_portal  # ← Explicitly specify DB name

# Collections
users = db.users
events = db.events
matches = db.matches
players = db.players