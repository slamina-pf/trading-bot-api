
from joblib import dump, load

def save_model(model, model_name, path=None):
    dump(model, f"{path}/{model_name}.joblib")

def load_model(model_name, path=None):
    return load(f"{path}/{model_name}.joblib")