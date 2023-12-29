import requests, os, smtplib, time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

FROM_ADDR = os.getenv('GMAIL_ACCOUNT')
TO_ADDRS = ['manch.hon@gmail.com',]
PYTHON_APP_GMAIL_CODE = os.getenv('PYTHON_APP_GMAIL_CODE')

MY_LAT = 37.774929 # Your latitude
MY_LONG = -122.419418 # Your longitude

def is_iss_overhead(lat=MY_LAT, lng=MY_LONG):
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    print(f'Current ISS latitude: {iss_latitude}  longitude: {iss_longitude}')
    print(f'My latitude: {lat}  longitude: {lng}')
    #Your position is within +5 or -5 degrees of the ISS position.
    return abs(iss_latitude - lat) < 5 and abs(iss_longitude - lng) < 5

def is_nighttime_now(lat=MY_LAT, lng=MY_LONG):
    parameters = {
        "lat": lat,
        "lng": lng,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    return time_now.hour < sunrise or time_now.hour > sunset

def send_reminder_mail(from_addr=FROM_ADDR, to_addrs=TO_ADDRS):
    msg = "Subject:ISS is visible now!\n\nHi, this is a friendly reminder that the ISS is currently over sky at your location and is visible now."
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=from_addr, password=PYTHON_APP_GMAIL_CODE)
        for recipent in to_addrs:
            connection.sendmail(from_addr=FROM_ADDR, to_addrs=recipent, msg=msg)
    

while True:
    if is_iss_overhead() and is_nighttime_now():
        send_reminder_mail()
        break
    else:
        print(f'Sleeping for 60 sec')
        time.sleep(60)
#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



