import os
from os.path import join, dirname
from dotenv import load_dotenv
import smtplib, datetime, random
import pandas as pd

BIRTHDAY_FILE = join(os.path.dirname(__file__), 'birthdays.csv')
LETTER_TEMPLATE_DIR = join(os.path.dirname(__file__), 'letter_templates')
load_dotenv()

GMAIL_ACCOUNT = os.getenv('GMAIL_ACCOUNT')
PYTHON_APP_GMAIL_CODE = os.getenv('PYTHON_APP_GMAIL_CODE')

# print(f'GMAIL_ACCOUNT: {GMAIL_ACCOUNT}')
# print(f'PYTHON_APP_GMAIL_CODE: {PYTHON_APP_GMAIL_CODE}')


##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv
# 2. Check if today matches a birthday in the birthdays.csv

df = pd.read_csv(BIRTHDAY_FILE)

now = datetime.datetime.now()
month = now.month
day = now.day

birthday_people = []
for row in df.iterrows():
    data = row[1]
    if data['month'] == month and data['day'] == day:
        birthday_people.append((data['name'], data['email']))

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

def send_mail(to_addrs, msg):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=GMAIL_ACCOUNT, password=PYTHON_APP_GMAIL_CODE)
        connection.sendmail(from_addr=GMAIL_ACCOUNT, 
                            to_addrs=to_addrs, 
                            msg=msg)

# 4. Send the letter generated in step 3 to that person's email address.

letter_files = os.listdir(LETTER_TEMPLATE_DIR)
# print(letters)
for name, email in birthday_people:
    letter_file = join(LETTER_TEMPLATE_DIR, random.choice(letter_files))
    with open(letter_file, 'r') as file:
        content = file.read()
    # print(content)
    send_mail(email, f"Subject:Happy Birthday!\n\n{content.replace('[NAME]', name)}")
