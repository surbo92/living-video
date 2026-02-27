import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(lat="40.4168", lon="-3.7038"):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
    r = requests.get(url)
    data = r.json()

    return {
        "is_day": data["current"]["is_day"],
        "rain": data["current"]["precip_mm"]
    }
