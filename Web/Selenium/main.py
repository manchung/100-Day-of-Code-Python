from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # Prevents browser from closing

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.python.org/')

li_elements = driver.find_elements(By.CSS_SELECTOR, value='.event-widget ul li')

event_dict = {}
for idx, li in enumerate(li_elements):
    date = li.find_element(By.TAG_NAME, value='time').text
    event = li.find_element(By.TAG_NAME, value='a').text
    # print(f'Event date: {date}  name: {event}')
    event_dict[idx] = {'time': date, 'name': event}

print(event_dict)
# driver.quit()