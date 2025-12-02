from flask import Blueprint, render_template, request, jsonify
from config import events, matches

coord_bp = Blueprint('coord', __name__)

@coord_bp.route('/login')
def login():
    return render_template('coord/login.html')

@coord_bp.route('/dashboard')
def dashboard():
    all_events = list(events.find({}, {'_id': 0}))
    all_matches = list(matches.find({}))
    return render_template('coord/dashboard.html', events=all_events, matches=all_matches)

@coord_bp.route('/api/schedule-match', methods=['POST'])
def schedule_match():
    data = request.get_json()
    match = {
        "event": data['event'],
        "team1": data['team1'],
        "team2": data['team2'],
        "date": data['date'],
        "status": "scheduled"
    }
    matches.insert_one(match)
    return jsonify({"success": True})