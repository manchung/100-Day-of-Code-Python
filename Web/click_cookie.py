from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # Prevents browser from closing

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://orteil.dashnet.org/experiments/cookie/')


cookie_element = driver.find_element(By.ID, value='cookie')
levels_ids = ['buyCursor', 'buyGrandma', 'buyFactory', 'buyMine', 'buyShipment', 'buyAlchemy lab', 'buyPortal', 'buyTime machine']
levels_ids.reverse()
duration = 60 * 5  # 5 minutes

def first_activated_level(ids):
    for id in ids:
        level = driver.find_element(By.ID, value=id)
        if level.get_attribute('class') != 'grayed':
            return level
    return None

def do_for_duration(duration, action):
    start_time = time.time()
    while time.time() - start_time < duration:
        action()
        time.sleep(0.1)


def click_cookie():
    for i in range(100):
        cookie_element.click()

def play_game(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        do_for_duration(5, click_cookie)
        buy_level = first_activated_level(levels_ids)
        if buy_level:
            buy_level.click()
        print(f'Time passed {time.time() - start_time}')


play_game(duration)

