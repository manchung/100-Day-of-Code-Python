import requests, os
from dotenv import load_dotenv

load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
NEWSAPI_API_KEY = os.getenv('NEWSAPI_API_KEY')
ALPHAVANTAGE_URL = 'https://www.alphavantage.co/query'
NEWSAPI_URL = 'https://newsapi.org/v2/everything'
# https://newsapi.org/v2/everything?q=tesla&from=2024-01-01&sortBy=publishedAt&language=en&searchin=title&apiKey=e374a0d315584cc8acca73f14ab7050a
STOCK = "AAPL"
COMPANY_NAME = "Apple"

alpha_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': ALPHAVANTAGE_API_KEY,
}


response = requests.get(ALPHAVANTAGE_URL, params=alpha_params)
response.raise_for_status()
stock_time_series = response.json()['Time Series (Daily)']

stock_keys = sorted(stock_time_series.keys(), reverse=True)
close_prices = [float(stock_time_series[stock_keys[0]]['4. close']), 
                float(stock_time_series[stock_keys[1]]['4. close'])]
# print(f'close_prices: {close_prices}')
price_delta = close_prices[0] - close_prices[1]
price_delta_percentage = price_delta / close_prices[1]

if abs(price_delta_percentage) > 0.01:
    newsapi_params = {
        'q': STOCK,
        'from': stock_keys[1],
        'sortBy': 'publishedAt',
        'language': 'en',
        # 'searchIn': 'title',
        'apiKey': NEWSAPI_API_KEY,
    }
    response = requests.get(NEWSAPI_URL, params=newsapi_params)
    response.raise_for_status()
    news_data = response.json()
    articles = news_data['articles'][0:5]
    if price_delta > 0:
        dir_symbol = '🔺'
    else:
        dir_symbol = '🔻'
    print(f'{STOCK} {dir_symbol}{price_delta_percentage*100:.0f}%')
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"{article['description']}")
        print('----------------------')




## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

