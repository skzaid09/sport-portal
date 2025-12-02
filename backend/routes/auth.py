from flask import Blueprint, request, jsonify, session
from models.user import get_user_by_username, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = get_user_by_username(username)
    if user and user['role'] == role and verify_password(password, user['password']):
        session['user'] = {'id': str(user['_id']), 'username': user['username'], 'role': user['role']}
        return jsonify({"success": True, "redirect": f"/{role}/dashboard"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})