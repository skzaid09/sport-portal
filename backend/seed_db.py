from config import users, events, matches
from models.user import hash_password

# Clear collections
users.delete_many({})
events.delete_many({})
matches.delete_many({})

# Insert events
events.insert_one({
    "name": "Annual Football Cup",
    "date": "2025-12-15",
    "description": "Inter-college football championship"
})

# Insert users with hashed passwords
users.insert_many([
    {"username": "admin1", "password": hash_password("admin123"), "role": "admin"},
    {"username": "coord1", "password": hash_password("coord123"), "role": "coord"},
    {"username": "player1", "password": hash_password("player123"), "role": "player"}
])

print("✅ Database seeded with test users & event!")