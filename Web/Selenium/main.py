from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://www.python.org/')

li_elements = driver.find_elements(By.CSS_SELECTOR, value='.event-widget ul li')
# print(li_elements)
# print(len(li_elements))

event_dict = {}
for idx, li in enumerate(li_elements):
    date = li.find_element(By.TAG_NAME, value='time').text
    event = li.find_element(By.TAG_NAME, value='a').text
    # print(f'Event date: {date}  name: {event}')
    event_dict[idx] = {'time': date, 'name': event}

print(event_dict)
driver.quit()