from dotenv import load_dotenv
import requests, os
from twilio.rest import Client

load_dotenv()

API_KEY=os.getenv('OPEN_WEATHER_MAP_API_KEY')
SF_LAT=37.774929
SF_LON=-122.419418

OWP_URL='https://api.openweathermap.org/data/2.5/forecast'

params={
    'lat': SF_LAT,
    'lon': SF_LON,
    # 'cnt': 4,
    'appid': API_KEY,
}

response = requests.get(OWP_URL, params=params)
response.raise_for_status()
weather_data = response.json()
# print(response.status_code)

for forecast in weather_data['list']:
    for weather in forecast['weather']:
        if int(weather['id']) < 700:
            print(f"id: {weather['id']}  main: {weather['main']}")
