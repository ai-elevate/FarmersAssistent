## main.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# Initialize Flask app
app = Flask(__name__)
Bootstrap(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmers_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy ORM
try:
    db = SQLAlchemy(app)
except Exception as e:
    print("Failed to initialize database. Error: ", str(e))
    exit(1)

# Import views after app is initialized to avoid circular imports
try:
    from farmers_assistant import views
except ImportError as e:
    print("Failed to import views. Error: ", str(e))
    exit(1)

# Create all database tables
try:
    db.create_all()
except Exception as e:
    print("Failed to create database tables. Error: ", str(e))
    exit(1)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print("Failed to run the app. Error: ", str(e))
        exit(1)
