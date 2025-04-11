import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from helpers.connections import BINANCE_NORMAL_CONNECTION

# Fetch historical OHLCV data
def fetch_ohlcv(symbol="BTC/USDT", timeframe="1m", limit=1000):
    data = BINANCE_NORMAL_CONNECTION.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# Main function
def get_data():
    print("Fetching data from Binance...")
    df = fetch_ohlcv()
    df.to_csv("trend_following_data.csv", index=False)
    return df
