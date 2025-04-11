
import ta

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
    print("sell_signal", sell_signal)
    df["label"] = 0  # Default: Hold / No action
    df.loc[buy_signal, "label"] = 1
    df.loc[sell_signal, "label"] = -1

    return df