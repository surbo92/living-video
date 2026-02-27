import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(lat="40.4168", lon="-3.7038"):
    try:
        if not API_KEY:
            return {"is_day": 1, "rain": 0.0, "source": "no_key"}

        url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
        r = requests.get(url, timeout=10)

        data = r.json()

        if "current" not in data:
            return {
                "is_day": 1,
                "rain": 0.0,
                "source": "api_error",
                "raw": data
            }

        return {
            "is_day": data["current"].get("is_day", 1),
            "rain": float(data["current"].get("precip_mm", 0.0)),
            "source": "ok"
        }

    except Exception as e:
        return {
            "is_day": 1,
            "rain": 0.0,
            "source": "exception",
            "error": str(e)
        }
