@echo off
cd backend
pip install -r requirements.txt
python seed_db.py
python app.py
pause