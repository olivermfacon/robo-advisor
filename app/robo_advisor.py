import os
import csv
import json
import datetime
import requests

from dotenv import load_dotenv

load_dotenv()

def to_usd(price):
    return "${0:,.2f}".format(price)

def process_urls():

    response = requests.get(url)
    parsed_response = json.loads(response.text) 
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

    print_info = {"symbol": symbols[count-1].upper(), "t_request": request_time, "t_refreshed": last_refreshed, "close": latest_close, "high": recent_high, "low": recent_low, "recommend": recommendation, "reason": reasoning}
    print_stocks(print_info)

def print_stocks(print_info):
    print("-------------------------")
    print("SELECTED SYMBOL: " + print_info["symbol"])
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + print_info["t_request"])
    print("-------------------------")
    print("LASTEST DAY: " + print_info["t_refreshed"])
    print("LATEST CLOSE: " + to_usd(float(print_info["close"])))
    print("RECENT HIGH: " + to_usd(float(print_info["high"])))
    print("RECENT LOW: " + to_usd(float(print_info["low"])))
    print("-------------------------")
    print("RECOMMENDATION: " + print_info["recommend"])           
    print("RECOMMENDATION REASON: " + print_info["reason"])    
    print("-------------------------")
    print("WRITING DATA TO CSV...")
    print("-------------------------")
    if count == ticker_count:
        print("HAPPY INVESTING!")
    else:
        print("-------------------------")
        print("-------------------------")
        print("-------------------------")
    print("-------------------------")

def to_csv():
    csv_file_name = symbols[count-1].lower() + "_prices.csv"
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", csv_file_name)

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

# MAIN BLOCK
##########################################
symbol_error = True
symbols = []
request_urls = []
count = 0

api_key = os.environ.get("api_key_env")

while True:
    symbol = input("Please enter a ticker number (type 'done' to load stocks): ").upper()
    
    if symbol == "DONE":
        break

    request_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    response = requests.get(request_url)
   
    test_parsed_response = json.loads(response.text)

    print(test_parsed_response["Meta Data"]["1. Information"])
    

    try:
        invalid_ticker_test = test_parsed_response["Meta Data"]["1. Information"] #testing whether I can access dictionary (check if ticker is vaiid)
        symbols.append(symbol)
        request_urls.append(request_url)
    except:
        print("INVALID STOCK SYMBOL. PLEASE TRY AGAIN.")


last_refreshed = test_parsed_response["Meta Data"]["3. Last Refreshed"]

ticker_count = len(request_urls)

for url in request_urls:
    count += 1
    process_urls()
    