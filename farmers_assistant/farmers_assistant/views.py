## views.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from farmers_assistant.main import app, db
from farmers_assistant.models import User, Weather, Advice, Reminder
from farmers_assistant.services import WeatherService, AdviceService, ReminderService
from werkzeug.security import check_password_hash

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    weather_service = WeatherService(Weather(location=current_user.location))
    weather_service.update_weather()
    advice_service = AdviceService(current_user.preferences)
    advices = advice_service.get_advice()
    reminder_service = ReminderService(current_user.reminders)
    reminders = reminder_service.get_reminders()
    return render_template('dashboard.html', weather=weather_service.weather, advices=advices, reminders=reminders)
