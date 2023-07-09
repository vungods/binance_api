from binance import Client, AsyncClient, BinanceSocketManager
from binance.exceptions import BinanceAPIException
from pprint import pformat
from binance.helpers import round_step_size
from binance.enums import *
import json

TEST_API_KEY = "38a8NZYdoKTqdQBvztjSDVI0kZUSuvA6tC0LDKohH5hPfE5S6QTxJWIe9FMZFj2q"
TEST_API_SECRET = "bTEGJyrHWKpPHSxfF3nXAu8ruZsbcXqYwlKnHDiI4mRKRNqH6VbB9ILsmTbQRYXc"
client = Client(api_key=TEST_API_KEY, api_secret=TEST_API_SECRET, testnet=True)


# Hàm lấy số lượng 1 token cụ thể trong tài khoản:
def get_asset_balance(asset, account_data):
    # account_data : client.get_account()
    for balance in account_data["balances"]:
        if balance["asset"] == asset:
            print(float(balance["free"]))
            return float(balance["free"])
    return None


# Hàm lấy số lượng toàn bộ token trong tài khoản:
def get_all_asset_balances(account_data):
    # account_data : client.get_account()
    balances = {}
    for balance in account_data["balances"]:
        asset = balance["asset"]
        free = float(balance["free"])
        balances[asset] = free
    return balances


def get_pandas_data(symbol: str, client_interval, start_date: str, end_date: str):
    # Lưu ý: binance chỉ cung cấp data khoảng 15 ngày gần nhất
    # symbol: "BTCUSDT","BNBUSDT"....
    # client_interval : Client.KLINE_INTERVAL_12HOUR,......
    #   start_date = "01 Jun, 2023"  # Ngày bắt đầu
    #   end_date = "22 Jun, 2023"  # Ngày kết thúc
    import pandas as pd
    import datetime

    klines = client.get_historical_klines(
        symbol, client_interval, start_str=start_date, end_str=end_date
    )
    df = pd.DataFrame(
        klines,
        columns=[
            "Open time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close time",
            "Quote asset volume",
            "Number of trades",
            "Taker buy base asset volume",
            "Taker buy quote asset volume",
            "Ignore",
        ],
    )
    df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
    df["Close time"] = pd.to_datetime(df["Close time"], unit="ms")
    return df


def order_market(symbol, quantity, order_type):
    import json

    if order_type == "buy":
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
    elif order_type == "sell":
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
    else:
        return "Invalid order type"

    # Get token balances
    balances = get_all_asset_balances(client.get_account())

    # Modify the order result
    order["tokenBalances"] = balances
    order["total_currentUSDT_balances"] = get_current_USDT_blance()
    # Tổng số USDT trong tài khoản (chỉ tính BNB nhân ra với USDT hiện cso, không tính các đồng khác, nếu đồng
    # khác mà giao dịch thì sẽ làm lệch số USDT đi => Tính sai)

    # Chuyển list trên thành định dạng json để lưu ra file log
    order_json = json.dumps(order)
    # Ghi ra file
    with open("transaction_history.log", "a") as file:
        file.write(f"{order_json}\n")

    return order


def get_current_USDT_blance():
    current_BNB = get_all_asset_balances(client.get_account()).get(
        "BNB"
    )  # Hàm lấy số lượng hiện tại của BNB
    current_BNB_USDT_avgprice = float(
        client.get_avg_price(symbol="BNBUSDT").get("price")
    )  # Lấy giá hiện tại
    current_BTC = get_all_asset_balances(client.get_account()).get(
        "BTC"
    )  # Hàm lấy số lượng hiện tại của BTC
    current_BTC_USDT_avgprice = float(
        client.get_avg_price(symbol="BTCUSDT").get("price")
    )  # Lấy giá hiện tại
    current_LTC = get_all_asset_balances(client.get_account()).get(
        "LTC"
    )  # Hàm lấy số lượng hiện tại của LTC
    current_LTC_USDT_avgprice = float(
        client.get_avg_price(symbol="LTCUSDT").get("price")
    )  # Lấy giá hiện tại
    current_XRP = get_all_asset_balances(client.get_account()).get(
        "XRP"
    )  # Hàm lấy số lượng hiện tại của XRP
    current_XRP_USDT_avgprice = float(
        client.get_avg_price(symbol="XRPUSDT").get("price")
    )  # Lấy giá hiện tại
    current_ETH = get_all_asset_balances(client.get_account()).get(
        "ETH"
    )  # Hàm lấy số lượng hiện tại của ETH
    current_ETH_USDT_avgprice = float(
        client.get_avg_price(symbol="ETHUSDT").get("price")
    )  # Lấy giá hiện tại
    current_USDT = get_all_asset_balances(client.get_account()).get(
        "USDT"
    )  # Số lượng USDT
    return (
        current_BNB * current_BNB_USDT_avgprice +
        current_BTC * current_BTC_USDT_avgprice +
        current_ETH * current_ETH_USDT_avgprice +
        current_XRP * current_XRP_USDT_avgprice +
        current_LTC * current_LTC_USDT_avgprice +
    + current_USDT
    )

def get_time(line):
    total = json.loads(line)
    print(total)
