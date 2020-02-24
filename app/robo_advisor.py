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

while True:
    symbol = input("Please enter a stock symbol: ")
    
    request_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
   
    api_key = os.environ.get("api_key_env")

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    
    response = requests.get(request_url)
    
    parsed_response = json.loads(response.text)

    try:
        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
        break
    except:
        print("INVALID STOCK SYMBOL. PLEASE TRY AGAIN.")

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []
#closing_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    #closing_price = tsd[date]["4. close"]
    high_prices.append(high_price)
    low_prices.append(low_price)
    #closing_prices.append(closing_price)

recent_high = max(high_prices)
recent_low = min(low_prices)

if float(latest_close) < 1.2*float(recent_low) and float(latest_close) > 0.8*float(recent_high):
    recommendation = "NO RECOMMENDATION"
    reasoning = "CANNOT ACCURATELY ESTIMATE IF STOCK IS UNDERVALUED OR OVERVALUED. LATEST CLOSING PRICE IS WITHIN 20% OF THE RECENT HIGH AND LOW." 
elif float(latest_close) < 1.2*float(recent_low):
    recommendation = "BUY!"
    reasoning = "THE STOCK IS LIKELY TO BE UNDERVALUED (THE CLOSING PRICE IS WITHIN 20% OF THE STOCK'S RECENT LOW)"
elif float(latest_close) > 0.8*float(recent_high):
    recommendation = "SELL!"
    reasoning = "THE STOCK IS LIKELY TO BE OVERVALUED (THE CLOSING PRICE IS WITHIN 20% OF THE STOCK'S RECENT HIGH)"
else:
    recommendation = "NO RECOMMENDATION"
    reasoning = "NO SPECIFIC DATA TO ESTIMATE FUTURE PERFORMANCE"

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol.upper()}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {request_time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {recommendation}")           
print(f"RECOMMENDATION REASON: {reasoning}")    
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
            csv_headers[0]: date,
            csv_headers[1]: to_usd(float(daily_prices["1. open"])),
            csv_headers[2]: to_usd(float(daily_prices["2. high"])),
            csv_headers[3]: to_usd(float(daily_prices["3. low"])),
            csv_headers[4]: to_usd(float(daily_prices["4. close"])),
            csv_headers[5]: daily_prices["5. volume"]
        })
    
# QUESTIONS FOR PROF ROSETTI
# 1. Is the try block okay to use?
# 2. Should the program keep asking for stock symbols until "DONE"
# 3. Is it alright to have no recommendation if closing is not near recent high or low?