from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import re

zillow_page = requests.get('https://appbrewery.github.io/Zillow-Clone').text

properties = []
soup = BeautifulSoup(zillow_page, 'html.parser')
property_tags = soup.select('.ListItem-c11n-8-84-3-StyledListCardWrapper')
for property_tag in property_tags:
    a_tag = property_tag.find('a')
    price_tag = property_tag.find(class_='PropertyCardWrapper')
    address_tag = property_tag.find('address')
    
    href_link = a_tag.get("href")
    price = re.split(r'[/+]', price_tag.getText().strip())[0]
    address = address_tag.getText().strip()
    if '|' in address:
        address = address.split('|')[1]
    # print(f'link: {href_link}  price: {price}  address: {address}')
    properties.append({
        'address': address,
        'price': price,
        'link': href_link})
    # titles.append(property_tag.getText(), a_tag.get("href")])

GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfqp1zuw5Td50dFFYSYhLtvH7lTyJQXxjx2BYuJYXQyOfoYlQ/viewform?usp=dialog'


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # Prevents browser from closing
# chrome_options.add_argument('user-data-dir="/Users/manchhon/Library/Application Support/Google/Chrome/Profile 1"')

driver = webdriver.Chrome(options=chrome_options)

for property in properties:
    driver.get(GOOGLE_FORM_URL)
    time.sleep(10)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')

    address_input.send_keys(property['address'])
    price_input.send_keys(property['price'])
    link_input.send_keys(property['link'])
    submit_button.click()
    



