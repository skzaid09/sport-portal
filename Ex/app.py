# backend/app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
from config import db, users_collection, events_collection, matches_collection
import qrcode
from io import BytesIO
import base64
import os  # ✅ THIS WAS MISSING — NOW ADDED!

app = Flask(__name__)

@app.route('/')
def home():
    qr_code_path = "static/qr_codes/portal_qr.png"
    
    # Create directory if not exists
    os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
    
    # Generate QR code if not exists
    if not os.path.exists(qr_code_path):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(request.url_root)  # URL of this app
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_code_path)

    # Read QR code as base64 to embed in HTML
    with open(qr_code_path, "rb") as f:
        qr_data = base64.b64encode(f.read()).decode('utf-8')

    return render_template('index.html', qr_code=qr_data)

@app.route('/login/<role>')
def login(role):
    if role not in ['admin', 'coord', 'player']:
        return "Invalid role", 400
    return render_template(f'{role}/login.html', role=role)

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = users_collection.find_one({"username": username, "role": role})
    if user and user.get("password") == password:  # ⚠️ For demo only! Use bcrypt in prod!
        return jsonify({"success": True, "redirect": f"/{role}/dashboard"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)