# from alpaca.trading.client import TradingClient

# print("Script started")

# try:
#     tradingclient = TradingClient("PK3RQUV82C5I35FW3K6L", "BJoE2Tg7RsZOkYVPdevRp9t4xjy1sgLguPKFH5JY", paper=True)
#     account = tradingclient.get_account()
#     print("Account Number:", account.account_number)
#     print("Buying Power:", account.buying_power)

# except Exception as e:
#     print("An error occurred:", e)

from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from datetime import datetime

data_client = StockHistoricalDataClient("PK3RQUV82C5I35FW3K6L","BJoE2Tg7RsZOkYVPdevRp9t4xjy1sgLguPKFH5JY")

request_param = StockTradesRequest(
    symbol_or_symbols = "AAPL",
    start = datetime(2025,4,8,14,30),
    end = datetime(2025,4,8,14,45)
)

trades = data_client.get_stock_trades(request_param)

print(trades)