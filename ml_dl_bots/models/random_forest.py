import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.collect_data import get_data
from feature_engineering.feature_engineering import clean_data
from helpers.models import load_model
import pandas as pd

def random_forest_model():
    df = get_data()
    df = clean_data(df)
    model = load_model("random_forest_model", path="ml_dl_bots/trained_models")

    latest_data = pd.DataFrame([df.iloc[-1][["sma_50", "sma_200", "ema_10", "rsi", "macd", "macd_signal", "macd_histogram"]]])

    rf_prediction = model.predict(latest_data)[0]
    
    print("Random Forest Prediction:", "BUY" if rf_prediction == 1 else "SELL")


if __name__ == "__main__":
    random_forest_model()