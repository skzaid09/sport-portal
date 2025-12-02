from flask import Blueprint, render_template, session, redirect, url_for
from config import matches, events

player_bp = Blueprint('player', __name__)

@player_bp.route('/login')
def login():
    return render_template('player/login.html')

@player_bp.route('/dashboard')
def dashboard():
    if 'user' not in session or session['user']['role'] != 'player':
        return redirect('/')
    all_events = list(events.find({}, {'_id': 0, 'password': 0}))
    all_matches = list(matches.find({}, {'_id': 0}))
    return render_template('player/dashboard.html', events=all_events, matches=all_matches)