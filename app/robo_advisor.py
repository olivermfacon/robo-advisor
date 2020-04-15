# app/robo_advisor.py
import csv
import json
import os
import datetime
import requests

#import plotly
#import plotly.graph_objs as go

def to_usd(price):
    return "${0:,.2f}".format(price)
    
def compile_url(symbol):
    api_key = os.environ.get("api_key_env")

    return f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"

def get_response(request_url):
    response = requests.get(request_url)
    return json.loads(response.text)

def divider():
    return "-------------------------"

def recommendation_and_reason(recent_low,recent_high,latest_close):
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
    recommendation_reasoning = [recommendation, reasoning]
    return recommendation_reasoning


if __name__ == "__main__":
    pre_valid_error = True


    while pre_valid_error == True:
        count = 0
        symbol = input("Please enter a stock symbol: ").upper()
        if symbol == "DONE":
            break

        for char in symbol:
            if char.isdigit(): #https://www.digitalocean.com/community/tutorials/how-to-use-break-continue-and-pass-statements-when-working-with-loops-in-python-3
                count += 1
        
        if count > 0:
            print("INVALID STOCK SYMBOL. PLEASE TRY AGAIN.")
        else:
            pre_valid_error = False


        if pre_valid_error == False:
            if len(symbol) < 1 or len(symbol) > 4:
                print("INVALID STOCK SYMBOL. PLEASE TRY AGAIN.")
                pre_valid_error = True
            else: 
                pre_valid_error = False

        if pre_valid_error == False:
            request_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            request_url = compile_url(symbol)

            parsed_response = get_response(request_url)

            try:
                last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
            except:
                pre_valid_error = True
                print("INVALID STOCK SYMBOL. PLEASE TRY AGAIN.")



    tsd = parsed_response["Time Series (Daily)"]

    dates = list(tsd.keys())

    latest_day = dates[0]

    latest_close = tsd[latest_day]["4. close"]

    high_prices = []
    low_prices = []
    closing_prices = []

    for date in dates:
        high_price = tsd[date]["2. high"]
        low_price = tsd[date]["3. low"]
        closing_price = tsd[date]["4. close"]
        high_prices.append(high_price)
        low_prices.append(low_price)
        closing_prices.append(closing_price)

    recent_high = max(high_prices[0:100])
    recent_low = min(low_prices[0:100])
    print(recent_high)
    print(recent_low)
    year_high = max(high_prices[0:252])
    year_low = min(low_prices[0:252])

    recommendation_reasoning = recommendation_and_reason(recent_low, recent_high, latest_close)

    print(divider())
    print(f"SELECTED SYMBOL: {symbol}")
    print(divider())
    print("REQUESTING STOCK MARKET DATA...")
    print(f"REQUEST AT: "+ request_time)
    print(divider())
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"YEAR HIGH : {to_usd(float(year_high))}")
    print(f"YEAR LOW : {to_usd(float(year_low))}")
    print(divider())
    print(f"RECOMMENDATION: {recommendation_reasoning[0]}")           
    print(f"RECOMMENDATION REASON: {recommendation_reasoning[1]}")    
    print(divider())
    print("WRITING DATA TO CSV...")
    print(divider())

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

