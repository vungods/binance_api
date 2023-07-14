# Cài !pip install python-binance
import time
from binance.enums import *
from functions import *
import json
TEST_API_KEY = '38a8NZYdoKTqdQBvztjSDVI0kZUSuvA6tC0LDKohH5hPfE5S6QTxJWIe9FMZFj2q'
TEST_API_SECRET = 'bTEGJyrHWKpPHSxfF3nXAu8ruZsbcXqYwlKnHDiI4mRKRNqH6VbB9ILsmTbQRYXc'
client = Client(api_key=TEST_API_KEY, api_secret=TEST_API_SECRET, testnet=True)
import json
from binance.client import Client
import datetime

def create_data_dict(data):
    data_dict = {
        "Open time": data[0],
        "Open": data[1],
        "High": data[2],
        "Low": data[3],
        "Close": data[4],
        "Volume": data[5],
        "Close time": data[6],
        "Quote asset volume": data[7],
        "Number of trades": data[8],
        "Taker buy base asset volume": data[9],
        "Taker buy quote asset volume": data[10],
        "Ignore": data[11],
        "Symbol": data[12],
        # Add more key-value pairs as needed
    }
    return data_dict


def save_multi_symbol_to_json(data, pairs):
    file_name = "multi_symbol.json"
    data_all = {}  # Create an empty dictionary to store all data_dict dictionaries
    with open(file_name, 'a') as file:
        for pair, pair_data in zip(pairs, data):
            data_dict = create_data_dict(pair_data)
            data_all[pair] = data_dict  # Add data_dict to data_all dictionary

        json.dump(data_all, file)
        file.write('\n')
def save_price_to_json(total_balance):
    file_name = "account_balance.json"
    with open(file_name, 'a') as file:
        json.dump(total_balance, file)
        file.write('\n')



trading_pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "LTCUSDT"]
api_key = '38a8NZYdoKTqdQBvztjSDVI0kZUSuvA6tC0LDKohH5hPfE5S6QTxJWIe9FMZFj2q'
api_secret = 'bTEGJyrHWKpPHSxfF3nXAu8ruZsbcXqYwlKnHDiI4mRKRNqH6VbB9ILsmTbQRYXc'
# Initialize Binance client
client = Client(api_key, api_secret)
print("Running")
while True:
    data = []
    for pair in trading_pairs:
        pair_data = client.get_historical_klines(pair, Client.KLINE_INTERVAL_3MINUTE, "3 min ago UTC")
        pair_data[0].append(pair)
        data.append(pair_data[0])
    save_multi_symbol_to_json(data, trading_pairs)
    current_balance = get_current_USDT_blance()
    total_balance = {"total": f"{current_balance}", "time": f"{datetime.datetime.now()}"}
    save_price_to_json(total_balance)
    time.sleep(30)
