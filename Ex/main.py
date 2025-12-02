# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import uvicorn
from bson import ObjectId

app = FastAPI(title="Sports Portal API")

# 🔗 Connect to local MongoDB
try:
    client = MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # Test connection
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ Could not connect to MongoDB: {e}")
    exit(1)

# Use database 'sportsdb'
db = client["sportsdb"]

# 📁 Collections
users_collection = db["users"]
events_collection = db["events"]
matches_collection = db["matches"]
leaderboard_collection = db["leaderboard"]


# 🧩 Pydantic Models
class QRLoginRequest(BaseModel):
    qr_code: str


# 🔐 API Endpoint: Verify QR Code (User Login)
@app.post("/api/verify-qr")
def verify_qr(request: QRLoginRequest):
    """
    Verifies a user via their unique QR code.
    Returns user details if valid, else throws 401 error.
    """
    user = users_collection.find_one({"qr_code": request.qr_code})
    if user:
        return {
            "success": True,
            "name": user["name"],
            "role": user["role"],  # Admin / Coordinator / Player
            "college_id": user["college_id"]
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid QR Code"
        )


# 🏠 Root Endpoint (Test API)
@app.get("/")
def home():
    return {
        "message": "Welcome to College Sport Activity Management Portal",
        "endpoints": [
            "/api/verify-qr (POST)",
            "/ (GET)"
        ]
    }


# ✅ Run the server directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)