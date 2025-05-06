from config import API_KEY, API_SECRET
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
def authenticate():
    try:
        trading_client = TradingClient(API_KEY,API_SECRET, paper=True)
        account = trading_client.get_account()
        if account.trading_blocked:
            print('Account is currently restricted from trading')
        print('Authentication successfull!!')
        print(f'Buying power for today: {account.buying_power}')
        print(f'Available case : {account.cash}')
    except Exception as e:
        print("Failed to authenticate with Alpaca:", e)
        return None


def main():
    alpaca = authenticate()
    if not alpaca:
        return

    # From here you can call your bot components like:
    # data_manager.run()
    # strategy_engine.run()
    # etc.

if __name__ == "__main__":
    main()
