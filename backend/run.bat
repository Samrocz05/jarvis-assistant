@echo off
REM Activate the virtual environment
venv\Scripts\activate

REM Run the Flask application
set FLASK_APP=backend\app.py
set FLASK_ENV=development
flask run
