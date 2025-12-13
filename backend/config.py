# backend/config.py
import os
from pymongo import MongoClient

# MUST use MONGO_URI from environment — no fallback to localhost
MONGO_URI = os.environ['MONGO_URI']  # ← No .get() — forces error if missing

client = MongoClient(MONGO_URI)
db = client.sports_portal  # Explicitly specify database name

# Collections
users = db.users
events = db.events
matches = db.matches
players = db.players