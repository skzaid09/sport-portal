# backend/seed_db.py
from config import users, events
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def seed_database():
    try:
        # Only seed if users collection is empty
        if users.count_documents({}) == 0:
            print("🌱 Seeding database...")
            
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
            print("✅ Database seeded successfully!")
        else:
            print("ℹ️ Database already seeded — skipping.")
    except Exception as e:
        print(f"❌ Seed failed: {e}")