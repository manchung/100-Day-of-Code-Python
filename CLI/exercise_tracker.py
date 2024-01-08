import requests, os
from dotenv import load_dotenv
from datetime import datetime 

load_dotenv()

NUTRITIONIX_APP_ID = os.getenv('NUTRITIONIX_APP_ID')
NUTRITIONIX_APP_KEY = os.getenv('NUTRITIONIX_APP_KEY')
SHEETY_TOKEN=os.getenv('SHEETY_TOKEN')

NUTRITIONIX_DOMAIN = 'https://trackapi.nutritionix.com'
EXERCISE_ENDPOINT = '/v2/natural/exercise'
SHEETY_ENDPOINT = 'https://api.sheety.co/41d9e90663286d6ba25ec3c11f92909f/myWorkouts/workouts'

headers = {
    'X-APP-ID': NUTRITIONIX_APP_ID,
    'X-APP-KEY': NUTRITIONIX_APP_KEY,
    # 'Content-Type': 'application/json',
}

query_params = {
    'query': input('Tell me which exercises you did: '),
}

response = requests.post(url=f'{NUTRITIONIX_DOMAIN}/{EXERCISE_ENDPOINT}', json=query_params, headers=headers)
print(response)
response.raise_for_status()

exercises = response.json()['exercises']
# print(f'Exercise duration: {exercise["duration_min"]}  name: {exercise["name"]} calories: {exercise["nf_calories"]}')

sheety_headers = {
    'Authorization': f'Bearer {SHEETY_TOKEN}'
}

now = datetime.now()
curr_date = now.strftime('%Y/%m/%d')
curr_time = now.strftime('%H:%M:%S')
for exercise in exercises:
    name = exercise['name']
    duration = exercise['duration_min']
    calories = exercise['nf_calories']
    sheety_params = {
        'workout': {
            'date': curr_date,
            'time': curr_time,
            'exercise': name.title(),
            'duration': duration,
            'calories': calories,
        }
    }
    response = requests.post(url=SHEETY_ENDPOINT, json=sheety_params, headers=sheety_headers)
    print(response.text)