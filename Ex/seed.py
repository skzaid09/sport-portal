# backend/seed.py
from config import users_collection, events_collection, matches_collection

# Clear existing data
users_collection.delete_many({})
events_collection.delete_many({})
matches_collection.delete_many({})

# Insert test users
users_collection.insert_many([
    {"username": "admin1", "password": "admin123", "role": "admin"},
    {"username": "coord1", "password": "coord123", "role": "coord"},
    {"username": "player1", "password": "player123", "role": "player"}
])

# Insert sample event
events_collection.insert_one({
    "name": "Basketball Tournament",
    "date": "2025-12-01",
    "description": "Annual inter-college basketball championship"
})

print("✅ Database seeded successfully!")