import requests
from twilio.rest import  Client
#Insert stock api key
STOCK_API_KEY = ""
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
#Insert News Api Key
NEWS_API_KEY = ''
#Insert Twilio SID 
TWILIO_SID = ''
#Insert Twilio Auth Token
TWILIO_AUTH_TOKEN = ''

#Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print("Yesterday closing", yesterday_closing_price)

#Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print("Day before yesterday closing", day_before_yesterday_closing_price)

#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

if abs(diff_percent) >= 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)

    three_articles = news_response.json()["articles"]
    print(three_articles)

formatted_articles = [f"Headline: {article['title']}. \nBrief: {article ['description']}" for article in three_articles]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

for article in formatted_articles:
    message = client.messages.create(
            body= article,
            from_="",
            to=""
    )
