import bcrypt
from config import users

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def create_user(username, password, role):
    if users.find_one({"username": username}):
        return None
    hashed = hash_password(password)
    user = {"username": username, "password": hashed, "role": role}
    users.insert_one(user)
    return user

def get_user_by_username(username):
    return users.find_one({"username": username})