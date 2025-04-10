import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import ta
from helpers.connections import BINANCE_NORMAL_CONNECTION

# Fetch historical OHLCV data
def fetch_ohlcv(symbol="BTC/USDT", timeframe="1m", limit=1000):
    data = BINANCE_NORMAL_CONNECTION.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# Compute technical indicators
def compute_indicators(df):
    df["sma_50"] = ta.trend.sma_indicator(df["close"], window=50)
    df["sma_200"] = ta.trend.sma_indicator(df["close"], window=200)
    df["ema_10"] = ta.trend.ema_indicator(df["close"], window=10)
    df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    df["macd"] = ta.trend.macd(df["close"])
    df["macd_signal"] = ta.trend.macd_signal(df["close"])
    df["macd_histogram"] = ta.trend.macd_diff(df["close"])
    return df

def create_labels(df):
    # Signal is '1' (buy) when:
    # - SMA 50 > SMA 200 (trend up)
    # - RSI > 55 (stronger momentum confirmation)
    # - MACD > MACD Signal (bullish crossover)
    buy_signal = (
        (df["sma_50"] > df["sma_200"]) &
        (df["rsi"] > 55) &
        (df["macd"] > df["macd_signal"])
    )

    # Signal is '-1' (sell) when:
    # - SMA 50 < SMA 200 (trend down)
    # - RSI < 45 (bearish momentum)
    # - MACD < MACD Signal (bearish crossover)
    sell_signal = (
        (df["sma_50"] < df["sma_200"]) &
        (df["rsi"] < 45) &
        (df["macd"] < df["macd_signal"])
    )

    df["label"] = 0  # Default: Hold / No action
    df.loc[buy_signal, "label"] = 1
    df.loc[sell_signal, "label"] = -1

    return df

# Main function
def get_data():
    print("Fetching data from Binance...")
    df = fetch_ohlcv()
    df = compute_indicators(df)
    df = create_labels(df)
    #df.to_csv("trend_following_data.csv", index=False)
    return df
