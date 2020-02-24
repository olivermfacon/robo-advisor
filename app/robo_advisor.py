# app/robo_advisor.py
import os
import csv
import json
import datetime
import requests

from dotenv import load_dotenv

load_dotenv()

def to_usd(price):
    return "${0:,.2f}".format(price)

symbol_error = True

while symbol_error == True:

    symbol = input("Please enter a stock symbol: ")

    request_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    api_key = os.environ.get("api_key_env")

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    response = requests.get(request_url)

    parsed_response = json.loads(response.text)

    try:
        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
        symbol_error = False
    except:
        print("INVALID STOCK SYMBOL. PLEASE TRY AGAIN.")



tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(high_price)
    low_prices.append(low_price)

recent_high = max(high_prices)
recent_low = min(low_prices)

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol.upper()}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {request_time}")
print("-------------------------")
print("LATEST DAY: " + last_refreshed)
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("WRITING DATA TO CSV...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open",  "high", "low", "close","volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above

    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": to_usd(float(daily_prices["1. open"])),
            "high": to_usd(float(daily_prices["2. high"])),
            "low": to_usd(float(daily_prices["3. low"])),
            "close": to_usd(float(daily_prices["4. close"])),
            "volume": daily_prices["5. volume"]
        })
    