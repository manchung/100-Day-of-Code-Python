from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # Prevents browser from closing

driver = webdriver.Chrome(options=chrome_options)
print('Loading speed test...')

driver.get('https://www.speedtest.net/')

go_button = driver.find_element(By.CLASS_NAME, value='start-text')
go_button.click()

print('Running speed test...')

time.sleep(60)
download_speed = driver.find_element(By.CLASS_NAME, value='download-speed').text
upload_speed = driver.find_element(By.CLASS_NAME, value='upload-speed').text
print(f'Download speed: {download_speed}  Upload speed: {upload_speed}')

driver.quit()
