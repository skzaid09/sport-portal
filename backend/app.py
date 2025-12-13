# backend/app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import qrcode
from io import BytesIO
import base64
import socket

app = Flask(__name__)
app.secret_key = "sports-portal-secret"

# Import routes (will fail if not found)
try:
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.coord import coord_bp
    from routes.player import player_bp
except ImportError as e:
    print(f"❌ Import Error: {e}")
    raise

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(coord_bp, url_prefix='/coord')
app.register_blueprint(player_bp, url_prefix='/player')

@app.route('/')
def home():
    try:
        # Use request.url_root for correct base URL
        base_url = request.url_root.rstrip('/')
        portal_url = f"{base_url}/roles"

        qr_path = os.path.join(app.static_folder, 'qr_codes', 'portal_qr.png')
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        
        if not os.path.exists(qr_path):
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(portal_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(qr_path)

        with open(qr_path, "rb") as f:
            qr_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        return render_template('index.html', qr_code=qr_b64, portal_url=portal_url)
    except Exception as e:
        print(f"❌ Home route error: {e}")
        return f"Server error: {e}", 500

@app.route('/roles')
def role_selection():
    try:
        return render_template('role_selection.html')
    except Exception as e:
        print(f"❌ Role selection error: {e}")
        return f"Server error: {e}", 500

# Auto-seed database on startup (free workaround for Render)
with app.app_context():
    try:
        from seed_db import seed_database
        seed_database()
    except Exception as e:
        print(f"⚠️ Auto-seed failed: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)