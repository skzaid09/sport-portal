from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from config import users, events

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login')
def login():
    return render_template('admin/login.html')

@admin_bp.route('/dashboard')
def dashboard():
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect('/')
    
    all_users = list(users.find({}, {'_id': 0, 'password': 0}))
    all_events = list(events.find({}, {'_id': 0}))
    
    return render_template('admin/dashboard.html', users=all_users, events=all_events)

@admin_bp.route('/api/delete-user', methods=['POST'])
def delete_user():
    if 'user' not in session or session['user']['role'] != 'admin':
        return jsonify({"success": False}), 403
        
    data = request.get_json()
    username = data.get('username')
    if username == 'admin1':
        return jsonify({"success": False, "message": "Cannot delete super admin"}), 400
        
    result = users.delete_one({"username": username})
    if result.deleted_count > 0:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "User not found"}), 404