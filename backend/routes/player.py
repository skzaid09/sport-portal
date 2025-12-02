# backend/routes/player.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime
from config import players  # ← Make sure 'players' collection exists in config.py

player_bp = Blueprint('player', __name__)

# Route: /player/register → Main registration page
@player_bp.route('/register')
def register():
    return render_template('player/register.html')

# Route: /player/register/single → Single player form
@player_bp.route('/register/single')
def register_single():
    return render_template('player/register_single.html')

# Route: /player/register/team → Team registration form
@player_bp.route('/register/team')
def register_team():
    return render_template('player/register_team.html')

# API: Save single player
@player_bp.route('/api/register-single', methods=['POST'])
def register_single_api():
    data = request.get_json()
    # Insert into MongoDB
    players.insert_one({
        "type": "single",
        "name": data['name'],
        "department": data['department'],
        "roll_no": data['roll_no'],
        "sport": data['sport'],
        "registered_at": datetime.utcnow()
    })
    return jsonify({"success": True, "message": "Single player registered!"})

# API: Save team
@player_bp.route('/api/register-team', methods=['POST'])
def register_team_api():
    data = request.get_json()
    # Insert team with list of players
    players.insert_one({
        "type": "team",
        "team_name": data['team_name'],
        "department": data['department'],
        "sport": data['sport'],
        "players": data['players'],  # List of {name, roll_no}
        "registered_at": datetime.utcnow()
    })
    return jsonify({"success": True, "message": "Team registered!"})