# store_data.py
# Purpose: Insert sample data into MongoDB for College Sports Portal

from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["sportsdb"]  # Database name

# Define collections
users_collection = db["users"]
events_collection = db["events"]
teams_collection = db["teams"]
matches_collection = db["matches"]
scores_collection = db["scores"]
leaderboard_collection = db["leaderboard"]
notifications_collection = db["notifications"]
qr_codes_collection = db["qr_codes"]

print("✅ Connected to MongoDB. Using database 'sportsdb'")

# 🔹 1. Insert a User (Admin)
admin_user = {
    "name": "Prof. Anwar Petal",
    "college_id": "FAC2025",
    "role": "Admin",
    "department": "Computer Engineering",
    "year": None,
    "email": "anwar.petal@college.edu",
    "phone": "+919876543210",
    "qr_code": "QRADMIN1001",
    "teams": [],
    "is_active": True,
    "created_at": "2025-04-05"
}
users_collection.insert_one(admin_user)
print("👤 Admin inserted:", admin_user["name"])

# 🔹 2. Insert a Coordinator
coordinator = {
    "name": "Neha Sharma",
    "college_id": "COORD101",
    "role": "Coordinator",
    "department": "Sports Dept",
    "year": None,
    "email": "neha@college.edu",
    "phone": "+918765432109",
    "qr_code": "QRCOORD101",
    "teams": ["CRICKET_A", "VOLLEYBALL_B"],
    "is_active": True,
    "created_at": "2025-04-05"
}
users_collection.insert_one(coordinator)
print("👤 Coordinator inserted:", coordinator["name"])

# 🔹 3. Insert a Player
player = {
    "name": "Shaikh Mohammed Zaid",
    "college_id": "23BIT55",
    "role": "Player",
    "department": "IT",
    "year": "Second Year",
    "email": "zaid@college.edu",
    "phone": "+917654321098",
    "qr_code": "QR23BIT55",
    "teams": ["CRICKET_A"],
    "is_active": True,
    "created_at": "2025-04-05"
}
users_collection.insert_one(player)
print("👤 Player inserted:", player["name"])

# 🔹 4. Create a Sports Event
event = {
    "event_name": "Inter-College Sports Week 2025",
    "sport_type": "Cricket",
    "status": "Upcoming",
    "start_date": "2025-04-10",
    "end_date": "2025-04-15",
    "venue": "Main Ground A",
    "max_teams": 8,
    "organizer_id": "FAC2025",
    "rules": "Standard college cricket rules",
    "created_at": "2025-04-01"
}
events_collection.insert_one(event)
print("🏆 Event inserted:", event["event_name"])

print("\n✅ All sample data inserted successfully!")
print("\n📋 All Users in Database:")
for user in users_collection.find():
    print(f" - {user['name']} ({user['role']})")