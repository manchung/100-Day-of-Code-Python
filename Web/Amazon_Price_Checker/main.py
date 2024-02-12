from bs4 import BeautifulSoup
import requests, os, pprint, smtplib
from dotenv import load_dotenv

URL = 'https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6'
THRESHOLD_PRICE = 100
headers = {
    'upgrade-insecure-requests' : '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'sec-ch-ua': '\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"macOS\"',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
    'x-forwarded-proto': 'https',
    'x-https': 'on',
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

pp = pprint.PrettyPrinter(indent=4)

print(response)
# with open('output.html', 'w') as f:
#     f.write(response.text)

soup = BeautifulSoup(response.text, 'lxml')
# titles = [tag.getText() for tag in soup.select('span .aok-offscreen')]
# print(titles)

price_tags = soup.select('span.aok-offscreen')
print(price_tags)
price = price_tags[0].getText().strip().replace('$','')
price = float(price)
print(price)

title_tags = soup.select('#productTitle')
title = title_tags[0].getText().strip()
print(title)

# exit(0)
if price < THRESHOLD_PRICE:
    load_dotenv()

    FROM_ADDR = os.getenv('GMAIL_ACCOUNT')
    TO_ADDRS = ['manch.hon@gmail.com',]
    PYTHON_APP_GMAIL_CODE = os.getenv('PYTHON_APP_GMAIL_CODE')

    subject = 'Amazon Price Alert!!'
    body = f'Hi,\n\nWe found the following cheap deals for you!\n\n'
    body += f'{title} is now ${price}\n'
    body += URL
    
    msg = f"Subject:{subject}\n\n{body}".encode('utf-8')
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=FROM_ADDR, password=PYTHON_APP_GMAIL_CODE)
        for recipent in TO_ADDRS:
            connection.sendmail(from_addr=FROM_ADDR, to_addrs=recipent, msg=msg)