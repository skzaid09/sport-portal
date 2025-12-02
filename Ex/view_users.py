# view_users.py
from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["sportsdb"]  # Your database name
users_collection = db["users"]

print("📋 ALL USERS IN DATABASE:\n")
for user in users_collection.find():
    print(f"Name       : {user['name']}")
    print(f"Role       : {user['role']}")
    print(f"College ID : {user['college_id']}")
    print(f"QR Code    : {user['qr_code']}")
    print(f"Teams      : {user.get('teams', [])}")
    print("-" * 40)