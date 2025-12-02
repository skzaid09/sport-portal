# generate_qr_codes.py
# Purpose: Generate QR code images for all users in MongoDB

import qrcode
from pymongo import MongoClient
import os

# Connect to local MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["sportsdb"]
users_collection = db["users"]

# Create folder to store QR codes
qr_folder = "../frontend/assets/qr_codes"
os.makedirs(qr_folder, exist_ok=True)

print("🔄 Generating QR codes for all users...")

# Fetch all users with QR codes
users = users_collection.find({"qr_code": {"$exists": True}})
count = 0

for user in users:
    qr_data = user["qr_code"]  # e.g., QR23BIT55
    name = user["name"]
    
    # Generate QR code
    img = qrcode.make(qr_data)
    
    # Save as PNG
    filename = f"{qr_data}.png"
    filepath = os.path.join(qr_folder, filename)
    img.save(filepath)
    
    print(f"✅ Generated: {filename} → {name}")
    count += 1

print(f"\n🎉 Successfully generated {count} QR code(s) in: /frontend/assets/qr_codes/")