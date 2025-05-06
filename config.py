import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Alpaca API credentials
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_API_SECRET")

# Trading thresholds
BUY_THRESHOLD = float(os.getenv("BUY_THRESHOLD", -0.05))
SELL_THRESHOLD = float(os.getenv("SELL_THRESHOLD", 0.10))

# Other config (can add more later)
