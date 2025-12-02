# === SAVE THIS AS: create_project.py ===
import os

# Project structure
structure = {
    "backend": {
        "app.py": '''from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import qrcode
from io import BytesIO
import base64
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.coord import coord_bp
from routes.player import player_bp

app = Flask(__name__)
app.secret_key = "sports-portal-secret"

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(coord_bp, url_prefix='/coord')
app.register_blueprint(player_bp, url_prefix='/player')

@app.route('/')
def home():
    qr_path = os.path.join(app.static_folder, 'qr_codes', 'portal_qr.png')
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)
    
    if not os.path.exists(qr_path):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(request.url_root)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_path)

    with open(qr_path, "rb") as f:
        qr_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    return render_template('index.html', qr_code=qr_b64)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
''',

        "config.py": '''from pymongo import MongoClient
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sports-portal-secret-key-2025'
    MONGO_URI = "mongodb://localhost:27017/sports_portal"

client = MongoClient(Config.MONGO_URI)
db = client.sports_portal

users = db.users
events = db.events
matches = db.matches
''',

        "seed_db.py": '''from config import users, events, matches
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

users.delete_many({})
events.delete_many({})
matches.delete_many({})

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

print("✅ Database seeded with test users & event!")
''',

        "requirements.txt": "Flask==3.0.3\npymongo==4.7.0\npython-dotenv==1.0.1\nqrcode[pil]==7.4.2\nbcrypt==4.1.3\n",

        "run.bat": '''@echo off
cd backend
pip install -r requirements.txt
python seed_db.py
python app.py
pause
''',

        "models": {
            "user.py": '''import bcrypt
from config import users

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def get_user_by_username(username):
    return users.find_one({"username": username})
'''
        },

        "routes": {
            "auth.py": '''from flask import Blueprint, request, jsonify, session
from models.user import get_user_by_username, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    user = get_user_by_username(username)
    if user and user['role'] == role and verify_password(password, user['password']):
        session['user'] = {
            'username': user['username'],
            'role': user['role']
        }
        return jsonify({
            "success": True,
            "redirect": f"/{role}/dashboard"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid username, password, or role"
        }), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})
''',

            "admin.py": '''from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
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
''',

            "coord.py": '''from flask import Blueprint, render_template, request, jsonify
from config import events, matches

coord_bp = Blueprint('coord', __name__)

@coord_bp.route('/login')
def login():
    return render_template('coord/login.html')

@coord_bp.route('/dashboard')
def dashboard():
    if 'user' not in session or session['user']['role'] != 'coord':
        return redirect('/')
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
''',

            "player.py": '''from flask import Blueprint, render_template, session, redirect, url_for
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
'''
        },

        "templates": {
            "index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Sports Portal</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
  <div class="container-fluid vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="text-center p-4 rounded shadow" style="max-width: 600px; background: white;">
      <h1 class="mb-3">🏆 Sports Management Portal</h1>
      <p>Scan the QR code below to access the portal on your phone.</p>
      
      <div class="my-4">
        <img src="data:image/png;base64,{{ qr_code }}" alt="QR Code" class="img-fluid" style="max-width: 250px;">
      </div>

      <div class="d-grid gap-2">
        <a href="/coord/login" class="btn btn-warning btn-lg">📋 Coordinator</a>
        <a href="/player/login" class="btn btn-success btn-lg">🏅 Player</a>
        <a href="/admin/login" class="btn btn-danger btn-lg">🔐 Admin</a>
      </div>
    </div>
  </div>
</body>
</html>
''',

            "admin": {
                "login.html": '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin Login</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body class="bg-dark">
  <div class="container-fluid vh-100 d-flex align-items-center justify-content-center">
    <div class="card p-4 shadow" style="max-width: 400px; width: 100%;">
      <h3 class="text-center text-danger mb-4">🔐 Admin Login</h3>
      <form id="loginForm">
        <div class="mb-3">
          <label for="username" class="form-label text-white">Username</label>
          <input type="text" class="form-control" id="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label text-white">Password</label>
          <input type="password" class="form-control" id="password" required>
        </div>
        <input type="hidden" id="role" value="admin">
        <button type="submit" class="btn btn-danger w-100">Login</button>
      </form>
      <div id="error" class="mt-3 text-danger" style="display:none;"></div>
    </div>
  </div>

  <script>
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      const role = document.getElementById('role').value;

      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, role })
      });

      const data = await res.json();

      if (data.success) {
        window.location.href = data.redirect;
      } else {
        document.getElementById('error').textContent = data.message;
        document.getElementById('error').style.display = 'block';
      }
    });
  </script>

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
''',

                "dashboard.html": '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin Dashboard</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-danger">
    <div class="container">
      <a class="navbar-brand" href="#">Admin Panel</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="nav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="#" onclick="logout()">Logout</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container mt-4">
    <h2>✅ Admin Dashboard</h2>
    <div class="row g-3">
      <div class="col-md-4">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5 class="card-title">Create Event</h5>
            <p class="card-text">Add new sports events to the system.</p>
            <button class="btn btn-light">Create</button>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5 class="card-title">Manage Users</h5>
            <p class="card-text">View, edit, or delete users.</p>
            <button class="btn btn-light">Manage</button>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-warning text-dark">
          <div class="card-body">
            <h5 class="card-title">Send Notifications</h5>
            <p class="card-text">Broadcast messages to all users.</p>
            <button class="btn btn-dark">Send</button>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-5">
      <h4>👥 User Management (Demo)</h4>
      <table class="table table-striped">
        <thead><tr><th>Username</th><th>Role</th><th>Action</th></tr></thead>
        <tbody>
          {% for user in users %}
          <tr>
            <td>{{ user.username }}</td>
            <td>{{ user.role }}</td>
            <td>
              {% if user.username != 'admin1' %}
                <button class="btn btn-sm btn-outline-danger" onclick="deleteUser('{{ user.username }}')">Delete</button>
              {% else %}
                <span class="badge bg-secondary">Protected</span>
              {% endif %}
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

  <script>
    function deleteUser(username) {
      if (confirm(`Are you sure you want to delete ${username}?`)) {
        fetch('/admin/api/delete-user', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username })
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            alert('User deleted!');
            location.reload();
          } else {
            alert(data.message || 'Failed to delete user');
          }
        });
      }
    }
  </script>
</body>
</html>
'''
            },

            "coord": {
                "login.html": '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Coordinator Login</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body class="bg-warning bg-opacity-10">
  <div class="container-fluid vh-100 d-flex align-items-center justify-content-center">
    <div class="card p-4 shadow" style="max-width: 400px; width: 100%;">
      <h3 class="text-center text-warning mb-4">📋 Coordinator Login</h3>
      <form id="loginForm">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" id="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" required>
        </div>
        <input type="hidden" id="role" value="coord">
        <button type="submit" class="btn btn-warning w-100">Login</button>
      </form>
      <div id="error" class="mt-3 text-danger" style="display:none;"></div>
    </div>
  </div>

  <script>
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      const role = document.getElementById('role').value;

      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, role })
      });

      const data = await res.json();

      if (data.success) {
        window.location.href = data.redirect;
      } else {
        document.getElementById('error').textContent = data.message;
        document.getElementById('error').style.display = 'block';
      }
    });
  </script>

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
''',

                "dashboard.html": '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Coordinator Dashboard</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
      <a class="navbar-brand" href="#">Coordinator Panel</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="nav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="#" onclick="logout()">Logout</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container mt-4">
    <h2>Schedule New Match</h2>
    <form id="matchForm" class="row g-3 mb-5">
      <div class="col-md-6">
        <label class="form-label">Event</label>
        <select class="form-select" id="event" required>
          {% for evt in events %}
            <option value="{{ evt.name }}">{{ evt.name }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="col-md-6">
        <label class="form-label">Match Date</label>
        <input type="date" class="form-control" id="date" required>
      </div>
      <div class="col-md-6">
        <input type="text" class="form-control" id="team1" placeholder="Team A" required>
      </div>
      <div class="col-md-6">
        <input type="text" class="form-control" id="team2" placeholder="Team B" required>
      </div>
      <div class="col-12">
        <button type="submit" class="btn btn-primary">Schedule Match</button>
      </div>
    </form>

    <h3>Scheduled Matches</h3>
    <div class="table-responsive">
      <table class="table table-striped">
        <thead><tr><th>Event</th><th>Teams</th><th>Date</th><th>Status</th></tr></thead>
        <tbody>
          {% for m in matches %}
          <tr>
            <td>{{ m.event }}</td>
            <td>{{ m.team1 }} vs {{ m.team2 }}</td>
            <td>{{ m.date }}</td>
            <td><span class="badge bg-info">{{ m.status }}</span></td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

  <script>
    document.getElementById('matchForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = {
        event: document.getElementById('event').value,
        team1: document.getElementById('team1').value,
        team2: document.getElementById('team2').value,
        date: document.getElementById('date').value
      };
      const res = await fetch('/coord/api/schedule-match', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data) });
      if (res.ok) {
        alert('Match scheduled!');
        location.reload();
      }
    });
  </script>
</body>
</html>
'''
            },

            "player": {
                "login.html": '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Player Login</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body class="bg-success bg-opacity-10">
  <div class="container-fluid vh-100 d-flex align-items-center justify-content-center">
    <div class="card p-4 shadow" style="max-width: 400px; width: 100%;">
      <h3 class="text-center text-success mb-4">🏅 Player Login</h3>
      <form id="loginForm">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" id="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" required>
        </div>
        <input type="hidden" id="role" value="player">
        <button type="submit" class="btn btn-success w-100">Login</button>
      </form>
      <div id="error" class="mt-3 text-danger" style="display:none;"></div>
    </div>
  </div>

  <script>
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      const role = document.getElementById('role').value;

      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, role })
      });

      const data = await res.json();

      if (data.success) {
        window.location.href = data.redirect;
      } else {
        document.getElementById('error').textContent = data.message;
        document.getElementById('error').style.display = 'block';
      }
    });
  </script>

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
''',

                "dashboard.html": '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Player Dashboard</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-success">
    <div class="container">
      <a class="navbar-brand" href="#">Player Portal</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="nav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="#" onclick="logout()">Logout</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container mt-4">
    <h2>Welcome, Player! 🏆</h2>
    <div class="row g-3">
      <div class="col-md-4">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5 class="card-title">Browse Sports</h5>
            <p class="card-text">View all available events and matches.</p>
            <a href="#" class="btn btn-light">Explore</a>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5 class="card-title">Register Event</h5>
            <p class="card-text">Sign up for upcoming tournaments.</p>
            <a href="#" class="btn btn-light">Register</a>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card bg-warning text-dark">
          <div class="card-body">
            <h5 class="card-title">View Results</h5>
            <p class="card-text">Check your team’s performance.</p>
            <a href="#" class="btn btn-dark">See Results</a>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-5">
      <h4>🏆 Leaderboard</h4>
      <table class="table table-striped">
        <thead><tr><th>Rank</th><th>Team</th><th>Points</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>Team Alpha</td><td>120</td></tr>
          <tr><td>2</td><td>Team Beta</td><td>95</td></tr>
          <tr><td>3</td><td>Team Gamma</td><td>80</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''
            }
        },

        "static": {
            "css": {
                "style.css": '''body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: #f8f9fa;
}

.navbar-brand {
  font-weight: bold;
  letter-spacing: 0.5px;
}

.card {
  transition: transform 0.2s;
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
'''
            },
            "js": {
                "main.js": '''function logout() {
    fetch('/api/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(() => {
        window.location.href = '/';
    })
    .catch(err => {
        console.error('Logout failed:', err);
        alert('Logout failed. Please try again.');
    });
}

function showToast(message, type = 'info') {
    const toastDiv = document.createElement('div');
    toastDiv.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
    toastDiv.setAttribute('role', 'alert');
    toastDiv.setAttribute('aria-live', 'assertive');
    toastDiv.setAttribute('aria-atomic', 'true');
    toastDiv.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    document.body.appendChild(toastDiv);
    const toast = new bootstrap.Toast(toastDiv, { delay: 3000 });
    toast.show();
    toastDiv.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toastDiv);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
'''
            },
            "qr_codes": {}  # This will be created as empty folder
        }
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content.strip())

if __name__ == "__main__":
    project_root = input("Enter project folder name (e.g., sports-portal): ").strip() or "sports-portal"
    create_structure(project_root, structure)
    print(f"✅ Project created in folder: {project_root}")
    print("📁 Next steps:")
    print("1. Install MongoDB (https://www.mongodb.com/try/download/community)")
    print("2. Open Command Prompt in the project folder")
    print("3. Run: cd backend && pip install -r requirements.txt")
    print("4. Run: python seed_db.py")
    print("5. Run: python app.py")
    print("6. Open http://localhost:5000 in your browser!")