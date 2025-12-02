from config import users, events, matches
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

users.delete_many({})
events.delete_many({})
matches.delete_many({})

events.insert_one({
    "name": "Annual Football Cup",
    "date": "2025-12-15",
    "description": "Inter-college football championship"
})

users.insert_many([
    {"username": "admin1", "password": hash_password("admin123"), "role": "admin"},
    {"username": "coord1", "password": hash_password("coord123"), "role": "coord"},
    {"username": "player1", "password": hash_password("player123"), "role": "player"}
])

print("✅ Database seeded with test users & event!")