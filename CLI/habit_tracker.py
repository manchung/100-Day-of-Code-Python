from dotenv import load_dotenv
import requests, os

load_dotenv()
PIXELA_TOKEN = os.getenv('PIXELA_TOKEN')
PIXELA_USERNAME = os.getenv('PIXELA_USERNAME')

pixela_endpoint = 'https://pixe.la/v1/users'

user_params = {
    "token": PIXELA_TOKEN, 
    "username": PIXELA_USERNAME, 
    "agreeTermsOfService": "yes", 
    "notMinor": "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f'{pixela_endpoint}/{PIXELA_USERNAME}/graphs'

headers = {
    'X-USER-TOKEN': PIXELA_TOKEN,
}

graph_params = {
    'id': 'graph1',
    'name': 'Video Lectures Watched',
    'unit': 'min',
    'type': 'int',
    'color': 'sora',
    'timezone': 'America/Los_Angeles',
}

# response = requests.post(url=graph_endpoint, json=graph_params, headers=headers)
# print(response.text)

pixel_endpoint = f'{graph_endpoint}/graph1'
pixel_params = {
    'date': '20240105',
    'quantity': '45',
}

# response = requests.post(url=pixel_endpoint, json=pixel_params, headers=headers)
# print(response.text)

pixel_update_endpoint = f'{graph_endpoint}/graph1/20240105'
pixel_update_params = {
    'quantity': '35',
}

# response = requests.put(url=pixel_update_endpoint, json=pixel_update_params, headers=headers)
# print(response.text)

response = requests.delete(url=pixel_update_endpoint, headers=headers)
print(response.text)
