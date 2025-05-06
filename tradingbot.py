from alpaca.trading.client import TradingClient

print("Script started")

try:
    tradingclient = TradingClient("PK3RQUV82C5I35FW3K6L", "BJoE2Tg7RsZOkYVPdevRp9t4xjy1sgLguPKFH5JY", paper=True)
    account = tradingclient.get_account()
    print("Authentication successfull")
    print("Account Number:", account.account_number)
    print("Buying Power:", account.buying_power)

except Exception as e:
    print("An error occurred:", e)


