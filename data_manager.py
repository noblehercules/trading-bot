from config import API_KEY, API_SECRET
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from datetime import datetime, timedelta

client = StockHistoricalDataClient(API_KEY, API_SECRET)

def get_symbols() -> list:
    """Returns a list of all pyttradable symbols"""
    trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
    request_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
    assets = trading_client.get_all_assets(request_params)
    
    symbols = [asset.symbol for asset in assets if asset.tradable]
    print(f"Found {len(symbols)} tradable symbols.")
    return symbols

def get_price_change(symbol: str, days: int = 7) -> float:
    """Returns percent change between average price over last `days` and the average of the previous `days`"""
    end_date = datetime.now() - timedelta(days=1)
    mid_date = end_date - timedelta(days=days)
    start_date = mid_date - timedelta(days=days)

    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start_date,
        end=end_date
    )

    bars = client.get_stock_bars(request_params).data.get(symbol, [])
    if len(bars) < days * 2:  # We need enough bars for two full periods
        print(f"Not enough data for {symbol}")
        return None

    # Split into two periods
    first_period = [bar.close for bar in bars if bar.t < mid_date]
    second_period = [bar.close for bar in bars if bar.t >= mid_date]

    if not first_period or not second_period:
        print(f"Incomplete data for {symbol}")
        return None

    avg_first = sum(first_period) / len(first_period)
    avg_second = sum(second_period) / len(second_period)

    percent_change = (avg_second - avg_first) / avg_first
    return percent_change


def get_top_movers(days: int = 30, top_n: int = 30, direction='losers') -> list[tuple[str, float]]:
    """Fetches tradable symbols and returns top `n` movers over given time period"""
    symbols = get_symbols()[:1000]  # Limit to first 200 symbols for performance
    changes = []
    
    for symbol in symbols:
        try:
            change = get_price_change(symbol, days)
            if change is not None:
                changes.append((symbol, change))
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    # Sort by change ascending for losers, descending for gainers
    sorted_changes = sorted(
        changes, key=lambda x: x[1], reverse=(direction == 'gainers')
    )

    top_movers = sorted_changes[:top_n]

    # Print nicely formatted output
    print(f"\nTop {top_n} {'gainers' if direction == 'gainers' else 'losers'} over the past {days} days:\n")
    print(f"{'Symbol':<10} {'Change (%)':>12}")
    print("-" * 24)
    for symbol, change in top_movers:
        print(f"{symbol:<10} {change * 100:>10.2f}%")

    return top_movers


get_top_movers(days=30, top_n=30, direction='losers')

