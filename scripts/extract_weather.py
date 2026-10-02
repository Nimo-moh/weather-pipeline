import requests
import json
from datetime import datetime
import os

def fetch_weather(city, lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_raw_data(city, data):
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/{city}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {filename}")
    
if __name__ == "__main__":
    cities = {
        "Hargeisa": (9.5600, 44.0650),
        "Nairobi": (-1.2864, 36.8172),
        "Addis_Ababa": (9.0250, 38.7469),
        "Mogadishu": (2.0469, 45.3182),
    }

    for city, (lat, lon) in cities.items():
        data = fetch_weather(city, lat, lon)
        save_raw_data(city, data)