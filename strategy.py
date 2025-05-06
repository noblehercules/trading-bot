from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from config import API_KEY, API_SECRET
from data_manager import get_top_movers,change 

# Initialize trading client
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)

def execute_strategy():
    # Get available cash
    account = trading_client.get_account()
    cash = float(account.cash)

   # Get top losers (can be any number, not just 30)
    top_losers = get_top_movers(days=30, top_n=30, direction='losers')

    # Dynamically compute split
    split_index = int(len(top_losers) * 0.4)
    top_40_pct = top_losers[:split_index]     # 40% largest losers
    bottom_60_pct = top_losers[split_index:]  # Remaining 60%

    # Allocate funds
    cash_top = cash * 0.6
    cash_bottom = cash * 0.4

    print(f"\nTotal cash: ${cash:.2f}")
    print(f"Allocating ${cash_top:.2f} to top 40%, ${cash_bottom:.2f} to bottom 60%.\n")

    def place_orders(group, cash_allocated):
        per_stock_cash = cash_allocated / len(group)
        for symbol, change in group:
            try:
                order = MarketOrderRequest(
                    symbol=symbol,
                    notional=round(per_stock_cash, 2),
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                )
                trading_client.submit_order(order)
                print(f"Placed order for {symbol}: ${per_stock_cash:.2f}")
            except Exception as e:
                print(f"Error placing order for {symbol}: {e}")

    place_orders(top_40_pct, cash_top)
    place_orders(bottom_60_pct, cash_bottom)
