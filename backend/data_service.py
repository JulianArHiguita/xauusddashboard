import requests
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API CONFIGURATION
API_KEY = "842dcd6700ba42ab9cdbeacd8c308a8e"
BASE_URL = "https://api.twelvedata.com"
SYMBOL = "XAU/USD"

def get_current_price():
    """
    Fetches the latest real-time price for XAUUSD via Twelve Data.
    """
    try:
        # Quote endpoint gives price, change, percent_change
        url = f"{BASE_URL}/quote?symbol={SYMBOL}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if "code" in data and data["code"] != 200:
            logger.error(f"TwelveData Error: {data.get('message')}")
            return None

        price = float(data["close"]) if "close" in data else float(data["price"])
        prev_close = float(data["previous_close"])
        change = float(data["change"])
        change_percent = float(data["percent_change"])

        return {
            "price": round(price, 2),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "currency": "USD"
        }
    except Exception as e:
        logger.error(f"Error fetching current price: {e}")
        return None

def get_historical_data(period="1mo", interval="1h"):
    """
    Fetches historical data via Twelve Data.
    param period: Not used directly by Twelve Data (controlled by outputsize), 
                  but kept for function signature compatibility.
    param interval: 1m, 5m, 15m, 1h, 1day, etc.
    """
    try:
        # Map simple intervals to Twelve Data format
        # 5m -> 5min, 15m -> 15min, 1h -> 1h
        td_interval = interval
        if interval == "5m": td_interval = "5min"
        elif interval == "15m": td_interval = "15min"
        
        # Outputsize: 100 candles covers most recent history needed
        # 500 allows for better EMA 200 calculation
        url = f"{BASE_URL}/time_series?symbol={SYMBOL}&interval={td_interval}&apikey={API_KEY}&outputsize=250"
        
        response = requests.get(url)
        data = response.json()
        
        if "code" in data and data["code"] != 200:
            logger.error(f"TwelveData History Error: {data.get('message')}")
            return None

        if "values" not in data:
            return None
            
        # Twelve Data returns newest first, Pandas wants oldest first usually for calcs
        raw_data = data["values"] # List of dicts
        
        df = pd.DataFrame(raw_data)
        
        # Convert columns to numeric
        cols = ["open", "high", "low", "close", "volume"]
        for c in cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c])
        
        # Handle Date
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # Rename columns to Capitalized for existing analysis logic (Open, High, Low, Close)
        df = df.rename(columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
            "datetime": "Datetime"
        })
        
        # Reverse to have oldest first (required for TA libs)
        df = df.iloc[::-1].reset_index(drop=True)
        
        return df

    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return None


