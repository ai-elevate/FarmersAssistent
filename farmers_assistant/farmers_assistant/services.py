## services.py
import os
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from farmers_assistant.models import Weather, Advice, Reminder
from datetime import datetime, timedelta

class WeatherService:
    def __init__(self, weather: Weather):
        self.weather = weather

    def update_weather(self):
        try:
            response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={self.weather.location}&appid={os.environ.get("OPEN_WEATHER_MAP_API_KEY")}')
            response.raise_for_status()
            data = response.json()
            self.weather.temperature = data['main']['temp']
            self.weather.humidity = data['main']['humidity']
            self.weather.forecast = data['weather'][0]['description']
        except requests.exceptions.RequestException as e:
            print(f"Error updating weather: {e}")

class AdviceService:
    def __init__(self, user_preferences: list):
        self.user_preferences = user_preferences

    def get_advice(self):
        advice_list = []
        for preference in self.user_preferences:
            try:
                response = requests.get(f'https://www.farmingwebsite.com/advice/{preference}')
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                advice = soup.find('div', class_='advice-content').text
                advice_list.append(Advice(advice=advice, source=f'https://www.farmingwebsite.com/advice/{preference}'))
            except requests.exceptions.RequestException as e:
                print(f"Error getting advice: {e}")
        return advice_list

class ReminderService:
    def __init__(self, reminders: list[Reminder]):
        self.reminders = reminders

    def get_reminders(self):
        current_time = datetime.now()
        upcoming_reminders = [reminder for reminder in self.reminders if reminder.date - current_time <= timedelta(days=1)]
        return upcoming_reminders
