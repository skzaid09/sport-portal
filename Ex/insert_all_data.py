# insert_all_data.py
from pymongo import MongoClient
import qrcode
import os

# Connect to local MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["sportsdb"]

# Collections
users_collection = db["users"]
events_collection = db["events"]
teams_collection = db["teams"]
matches_collection = db["matches"]
scores_collection = db["scores"]
leaderboard_collection = db["leaderboard"]
notifications_collection = db["notifications"]

print("🔄 Inserting test data into sportsdb...")

# --- 1. Clear existing data ---
collections = [users_collection, events_collection, teams_collection, 
               matches_collection, scores_collection, leaderboard_collection, notifications_collection]

for collection in collections:
    collection.delete_many({})

print("✅ Cleared old data from all collections.")

# --- 2. Insert Users ---
test_users = [
    {
        "name": "Prof. Anwar Petal",
        "college_id": "FAC2025",
        "role": "Admin",
        "department": "Computer Engineering",
        "email": "anwar.petal@college.edu",
        "phone": "+919876543210",
        "qr_code": "QRADMIN1001",
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

users_collection.insert_many(test_users)
print(f"✅ Inserted {len(test_users)} users.")

# --- 3. Insert Event ---
event = {
    "event_name": "Inter-College Cricket Cup 2025",
    "sport_type": "Cricket",
    "status": "Ongoing",
    "start_date": "2025-04-10",
    "end_date": "2025-04-15",
    "venue": "Main Ground A",
    "max_teams": 8,
    "organizer_id": "FAC2025",
    "created_at": "2025-04-01"
}
event_result = events_collection.insert_one(event)
event_id = event_result.inserted_id
print("✅ Event created:", event["event_name"])

# --- 4. Insert Teams ---
team_a = {
    "team_name": "Team Thunder",
    "event_id": str(event_id),
    "sport_type": "Cricket",
    "captain_id": "23BIT55",
    "members": [
        {"user_id": "23BIT55", "name": "Zaid", "is_captain": True},
        {"user_id": "23BIT56", "name": "Ali", "is_captain": False}
    ],
    "total_players": 2,
    "college_dept": "IT"
}

team_b = {
    "team_name": "Team Flash",
    "event_id": str(event_id),
    "sport_type": "Cricket",
    "captain_id": "23BIT60",
    "members": [
        {"user_id": "23BIT60", "name": "Rahul", "is_captain": True},
        {"user_id": "23BIT61", "name": "Vikas", "is_captain": False}
    ],
    "total_players": 2,
    "college_dept": "CS"
}

teams_collection.insert_one(team_a)
teams_collection.insert_one(team_b)
print("✅ Two teams registered.")

# --- 5. Insert Match ---
match = {
    "event_id": str(event_id),
    "sport_type": "Cricket",
    "team_a": "Team Thunder",
    "team_b": "Team Flash",
    "scheduled_time": "2025-04-11T10:00:00Z",
    "venue": "Main Ground A",
    "status": "Completed",
    "winner": None,
    "round": "Group Stage"
}
match_result = matches_collection.insert_one(match)
match_id = match_result.inserted_id
print("✅ Match scheduled between Team Thunder vs Team Flash")

# --- 6. Insert Score (Manually Entered After Match) ---
score = {
    "match_id": str(match_id),
    "team_a_score": 120,
    "team_b_score": 95,
    "wickets_lost_a": 4,
    "wickets_lost_b": 8,
    "overs_played": "20.0",
    "winner": "Team Thunder",
    "entered_by": "COORD101",
    "entry_time": "2025-04-11T11:30:00Z",
    "status": "Final"
}
scores_collection.insert_one(score)

# Update match with winner
matches_collection.update_one(
    {"_id": match_result.inserted_id},
    {"$set": {"winner": "Team Thunder", "status": "Completed"}}
)
print("✅ Match result entered manually.")

# --- 7. Update Leaderboard ---
leaderboard = {
    "event_id": str(event_id),
    "rankings": [
        {"team_name": "Team Thunder", "wins": 1, "losses": 0, "points": 3},
        {"team_name": "Team Flash", "wins": 0, "losses": 1, "points": 0}
    ],
    "last_updated": "2025-04-11T11:35:00Z"
}
leaderboard_collection.insert_one(leaderboard)
print("✅ Leaderboard updated.")

# --- 8. Send Notification ---
notification = {
    "user_id": "23BIT55",
    "title": "Match Result Updated!",
    "message": "Your team won against Team Flash with a score of 120/4.",
    "type": "Match Result",
    "is_read": False,
    "sent_at": "2025-04-11T11:40:00Z"
}
notifications_collection.insert_one(notification)
print("✅ Notification sent to player.")

# --- 9. Generate QR Code Images ---
qr_folder = "../frontend/assets/qr_codes"
os.makedirs(qr_folder, exist_ok=True)

for user in users_collection.find({"qr_code": {"$exists": True}}):
    img = qrcode.make(user["qr_code"])
    img.save(f"{qr_folder}/{user['qr_code']}.png")
    print(f"✅ Generated QR code: {user['qr_code']}.png")

print("\n🎉 ALL DATA INSERTED SUCCESSFULLY!")
print("👉 Now start FastAPI server: uvicorn main:app --reload")