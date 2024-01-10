from dotenv import load_dotenv
import requests, os, datetime, smtplib
import urllib.parse


load_dotenv()

ORIGIN='SFO'

TEQUILA_API_KEY = os.getenv('TEQUILA_API_KEY')
SHEETY_TOKEN = os.getenv('SHEETY_TOKEN')
TEQUILA_SERVER = 'https://api.tequila.kiwi.com'
LOCATIONS_ENDPOINT = '/locations/query'
SEARCH_ENDPOINT = '/v2/search'
TEQUILA_HEADERS = {
    'apikey': TEQUILA_API_KEY,
    'accept': 'application/json',
}


SHEETY_SERVER = 'https://api.sheety.co/41d9e90663286d6ba25ec3c11f92909f/flightDeals'
PRICE_ENDPOINT = '/prices'
USER_ENDPOINT = '/users'
SHEETY_HEADERS = {
    'Authorization': f'Bearer {SHEETY_TOKEN}'
}

FROM_ADDR = os.getenv('GMAIL_ACCOUNT')
TO_ADDRS = ['manch.hon@gmail.com',]
PYTHON_APP_GMAIL_CODE = os.getenv('PYTHON_APP_GMAIL_CODE')


def searchCode(city):
    
    search_params = {
        'term': city,
        'locale': 'en-US',
        'location_types': 'city',
        'limit': 1,
        'active_only': 'true',
    }
    response = requests.get(url=f'{TEQUILA_SERVER}{LOCATIONS_ENDPOINT}', 
                            params=urllib.parse.urlencode(search_params, quote_via=urllib.parse.quote), 
                            headers=TEQUILA_HEADERS)
    response.raise_for_status()

    for loc in response.json()['locations']:
        return loc['code']
    return None
    


def setCode(id, code):
    # print(f'id: {id}  code: {code}')
    params = {
        'price': {
            'iataCode': code,
        }
    }
    response = requests.put(url=f'{SHEETY_SERVER}{PRICE_ENDPOINT}/{id}', json=params, headers=SHEETY_HEADERS)
    response.raise_for_status()
    # print(response)

def inspectCode():
    response = requests.get(url=f'{SHEETY_SERVER}{PRICE_ENDPOINT}', headers=SHEETY_HEADERS)
    response.raise_for_status()
    # print(response)
    # print(response.json())

    prices = response.json()['prices']
    for price in prices:
        # print(f"city: {price['city']}  iataCode: {price['iataCode']}")
        if price['iataCode'] is None or len(price['iataCode']) == 0:
            code = searchCode(price['city'])
            # print(f'Found code: {code}')
            if code is not None:
                setCode(price['id'], code)

'''
searchOneFlight returns the following dictionary:
{
    'price': 
    'airlines': 
    'local_departure':
    'departure_city':
    'departure_airport_code':
    'arrival_city':
    'arrival_airport_code':
}
'''
def searchOneFlight(origin, destination, date_from, date_to):
    params = {
        'fly_from': origin,
        'fly_to': destination,
        'date_from': date_from,
        'date_to': date_to,
        'curr': 'USD',
        # 'limit': 10,
    }
    response = requests.get(url=f'{TEQUILA_SERVER}{SEARCH_ENDPOINT}',
                            params=urllib.parse.urlencode(params, quote_via=urllib.parse.quote), headers=TEQUILA_HEADERS)
    response.raise_for_status()
    # print(response)
    search_results = []
    for flight in response.json()['data']:
       departure_time = flight['local_departure']
       departure_date, departure_time = departure_time.split('T')
    #    departure_time, _ = departure_time.split('.')
    #    departure_hour, departure_min, _ = departure_time.split(':')
       one_result = {
            'price': int(flight['price']),
            'airlines': flight['airlines'],
            'local_departure': departure_date,
            'departure_city': flight['cityFrom'],
            'departure_airport_code': flight['flyFrom'],
            'arrival_city': flight['cityTo'],
            'arrival_airport_code': flight['flyTo'],
       }

       search_results.append(one_result)
    
    # print(search_results)
    if len(search_results) > 0:
        return min(search_results, key=lambda x: x['price'])
    else:
        return None

def searchFlights():
    response = requests.get(url=f'{SHEETY_SERVER}{PRICE_ENDPOINT}', headers=SHEETY_HEADERS)
    response.raise_for_status()

    now = datetime.datetime.now()
    six_months_from_now = now + datetime.timedelta(days=180)

    date_from = now.strftime('%d/%m/%Y')
    date_to = six_months_from_now.strftime('%d/%m/%Y')

    flights = []
    prices = response.json()['prices']
    for price in prices:
        print(f"Searching flights for city: {price['city']}")
        if price['lowestPrice'] is None: 
            continue
        lowestPrice = price['lowestPrice']
        code = price['iataCode']
        cheapest_flight = searchOneFlight(ORIGIN, code, date_from, date_to)
        if cheapest_flight['price'] < int(lowestPrice):
            # print(f'Cheapest flight from {ORIGIN} to {code}: {cheapest_flight}')
            flights.append(cheapest_flight)
    return flights


def mailFlights(flights, to_name, to_addrs=TO_ADDRS):
    if len(flights) == 0:
        return
    
    subject = 'Cheap Flights Alert!!'
    body = f'Hi {to_name},\n\nWe found the following cheap flights for you!\n\n'

    for flight in flights:
        body += f"Only ${flight['price']} to fly from {flight['departure_city']}-{flight['departure_airport_code']} to {flight['arrival_city']}-{flight['arrival_airport_code']} on {flight['local_departure']}. Airlines: {' '.join(flight['airlines'])}\n\n"
    
    msg = f"Subject:{subject}\n\n{body}"
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=FROM_ADDR, password=PYTHON_APP_GMAIL_CODE)
        for recipent in to_addrs:
            connection.sendmail(from_addr=FROM_ADDR, to_addrs=recipent, msg=msg)

def signUp():
    print("Welcome to Manch's Flight Club!")
    print("We find the best flight deals and email you.")
    first_name = input("What is your first name?\n")
    last_name = input("What is your last name?\n")
    
    got_email = False
    while not got_email:
        email = input("What is your email?\n")
        verify_email = input("Type your email again.\n")
        if email == verify_email:
            got_email = True
    
    params = {
        'user': {
            'lastName': last_name,
            'firstName': first_name,
            'email': email,
        }
    }
    response = requests.post(url=f'{SHEETY_SERVER}{USER_ENDPOINT}', json=params, headers=SHEETY_HEADERS)
    response.raise_for_status()

    print("You're in the club!")

'''
getUsers will return a dictionary of the followng format:
{
    'firstName':
    'lastName':
    'email':
}
'''
def getUsers():
    response = requests.get(url=f'{SHEETY_SERVER}{USER_ENDPOINT}', headers=SHEETY_HEADERS)
    response.raise_for_status()
    return response.json()['users']

def main():
    inspectCode()
    flights = searchFlights()
    users = getUsers()

    for user in users:
        print(f"Emailing user {user['firstName']}")
        mailFlights(flights, to_name=user['firstName'], to_addrs=[user['email'],])

main()
# signUp()
