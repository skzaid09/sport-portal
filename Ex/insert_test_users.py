# insert_test_users.py
# Purpose: Insert sample users (Admin, Coordinator, Player) into MongoDB

from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["sportsdb"]  # Database name
users_collection = db["users"]

# Sample users to insert
test_users = [
    {
        "name": "Prof. Anwar Petal",
        "college_id": "FAC2025",
        "role": "Admin",
        "department": "Computer Engineering",
        "email": "anwar.petal@college.edu",
        "phone": "+919876543210",
        "qr_code": "QRADMIN1001",
        "teams": [],
        "is_active": True
    },
    {
        "name": "Neha Sharma",
        "college_id": "COORD101",
        "role": "Coordinator",
        "department": "Sports Dept",
        "email": "neha@college.edu",
        "phone": "+918765432109",
        "qr_code": "QRCOORD101",
        "teams": ["CRICKET_A", "VOLLEYBALL_B"],
        "is_active": True
    },
    {
        "name": "Shaikh Mohammed Zaid",
        "college_id": "23BIT55",
        "role": "Player",
        "department": "IT",
        "year": "Second Year",
        "email": "zaid@college.edu",
        "phone": "+917654321098",
        "qr_code": "QR23BIT55",
        "teams": ["CRICKET_A"],
        "is_active": True
    }
]

# Clear old data (optional)
users_collection.delete_many({})

# Insert new users
result = users_collection.insert_many(test_users)
print(f"✅ Successfully inserted {len(result.inserted_ids)} test users into MongoDB!")
print("🔐 QR Codes available:")
for user in test_users:
    print(f"   • {user['name']} → QR Code: {user['qr_code']}")