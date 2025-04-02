import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from helpers.collect_data import get_data
from feature_engineering.feature_engineering import clean_data
from helpers.models import save_model

def random_forest_training():
    df = get_data()

    data_cleaned = clean_data(df)
    
    features = ["sma_50", "sma_200", "ema_10", "rsi", "macd", "macd_signal", "macd_histogram"]
    X = data_cleaned[features]
    Y = data_cleaned["label"]

    # Split data into training & testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, Y_train)

    rf_preds = rf_model.predict(X_test)

    print("Random Forest Accuracy:", accuracy_score(Y_test, rf_preds))
    print("Random Forest Classification Report:\n", classification_report(Y_test, rf_preds))

    save_model(rf_model, "random_forest_model", path="ml_dl_bots/models")
    print("Model saved as random_forest_model.joblib")
if __name__ == "__main__":
    random_forest_training()