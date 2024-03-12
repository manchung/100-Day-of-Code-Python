from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# driver.get('https://en.wikipedia.org/wiki/Main_Page')

# stat_tag = driver.find_element(By.CSS_SELECTOR, value='#articlecount a[title="Special:Statistics"]')
# print(stat_tag.text)

driver.get('http://secure-retreat-92358.herokuapp.com/')
fName = driver.find_element(By.NAME, value='fName')
fName.send_keys('Horn')
lName = driver.find_element(By.NAME, value='lName')
lName.send_keys('Bozo')
email = driver.find_element(By.NAME, value='email')
email.send_keys('bozo@me.com')

button = driver.find_element(By.TAG_NAME, value='button')
button.click()

# driver.quit()