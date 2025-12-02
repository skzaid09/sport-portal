from pymongo import MongoClient

# Connect to local MongoDB (running on default port 27017)
client = MongoClient("mongodb://127.0.0.1:27017")

# Test if connection works
try:
    # This command checks if the server is available
    client.admin.command('ping')
    print("✅ SUCCESS: Connected to MongoDB!")

    # Use database 'sportsdb' (created automatically when data is added)
    db = client['sportsdb']

    # Use collection 'users' (like a table)
    users_collection = db['users']

    # Sample document to insert (e.g., an admin user)
    sample_user = {
        "name": "Prof. Anwar Petal",
        "role": "Admin",
        "college_id": "FAC2025",
        "department": "Computer Engineering",
        "qr_code": "QRADMIN1001"
    }

    # Insert the document
    result = users_collection.insert_one(sample_user)
    print(f"📄 Inserted test user with ID: {result.inserted_id}")

    # Optional: Print all users in the collection
    print("\n📋 All users in the database:")
    for user in users_collection.find():
        print(user)

except Exception as e:
    print("❌ ERROR: Could not connect to MongoDB or insert data.")
    print(f"   Details: {e}")
    print("\n💡 Possible fixes:")
    print("   1. Make sure MongoDB service is running (use 'net start MongoDB')")
    print("   2. Ensure 'pymongo' is installed: pip install pymongo")
    print("   3. Check that folder C:\\data\\db exists and has permissions")

finally:
    # Always close the connection
    client.close()