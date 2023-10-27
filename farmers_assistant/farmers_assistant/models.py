## models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(100), unique=True, nullable=False)
    preferences = db.relationship('Preference', backref='user', lazy=True)

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email

    def add_preference(self, preference: str):
        self.preferences.append(Preference(name=preference, user_id=self.id))

    def remove_preference(self, preference: str):
        pref = Preference.query.filter_by(name=preference, user_id=self.id).first()
        if pref:
            self.preferences.remove(pref)

class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    forecast = db.Column(db.String(100), nullable=False)

    def __init__(self, location: str):
        self.location = location

    def update_weather(self):
        raise NotImplementedError("This method should be implemented in services.py")

class Advice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advice = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(100), nullable=False)

    def __init__(self, advice: str, source: str):
        self.advice = advice
        self.source = source

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reminder = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, reminder: str, date: datetime):
        self.reminder = reminder
        self.date = date
