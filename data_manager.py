from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from datetime import datetime, timedelta
import os

# Load keys from environment
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_API_SECRET")

client = StockHistoricalDataClient(API_KEY, API_SECRET)


def get_symbols(limit=100) -> list:
    """Returns a list of tradable US equity symbols (limit can be changed)"""
    trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
    request_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
    assets = trading_client.get_all_assets(request_params)
    
    symbols = [asset.symbol for asset in assets if asset.tradable]
    print(f"Found {len(symbols)} tradable symbols. Using top {limit}.")
    return symbols[:limit]


def get_price_change(symbol: str, days: int = 7) -> float:
    """
    Returns percent change in average price between two `days`-long periods.
    First period: days X to days Y (older)
    Second period: most recent `days`
    """
    today = datetime.now()
    buffer_days = days * 2 + 10  # holiday & weekend buffer
    start_date = today - timedelta(days=buffer_days)

    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start_date,
        end=today,
        feed='iex'  # ✅ use IEX feed
    )

    try:
        bars = client.get_stock_bars(request_params).data.get(symbol, [])
    except Exception as e:
        print(f"Error fetching bars for {symbol}: {e}")
        return None

    if len(bars) < days + 5:  # be lenient
        print(f"{symbol}: only {len(bars)} bars found (need {days + 5})")
        return None

    # Sort bars by time to ensure order
    bars.sort(key=lambda bar: bar.timestamp)

    # Split data
    midpoint = len(bars) // 2
    first_half = bars[:midpoint]
    second_half = bars[midpoint:]

    first_avg = sum(bar.close for bar in first_half) / len(first_half)
    second_avg = sum(bar.close for bar in second_half) / len(second_half)

    return (second_avg - first_avg) / first_avg


def get_top_movers(days: int = 30, top_n: int = 30, direction: str = 'losers') -> list:
    """
    Fetches tradable symbols and returns top `n` movers.
    direction: 'gainers' or 'losers'
    """
    symbols = get_symbols(limit=100)  # test on 100 for speed
    changes = []

    for symbol in symbols:
        try:
            change = get_price_change(symbol, days)
            if change is not None:
                changes.append((symbol, change))
        except Exception as e:
            print(f"Error for {symbol}: {e}")

    # Sort results
    sorted_changes = sorted(
        changes,
        key=lambda x: x[1],
        reverse=(direction == 'gainers')
    )

    top_movers = sorted_changes[:top_n]

    # Output
    print(f"\nTop {top_n} {direction} over the past {days} days:\n")
    print(f"{'Symbol':<10} {'Change (%)':>12}")
    print("-" * 24)
    for symbol, change in top_movers:
        print(f"{symbol:<10} {change * 100:>10.2f}%")

    return top_movers



# Run for 30-day losers
get_top_movers(days=30, top_n=30, direction='losers')
