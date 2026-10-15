from pathlib import Path
import joblib
import pandas as pd


FEATURES = ["Area_sqft","Bedrooms","Bathrooms","Age_years","Distance_city_km"]

_model = None

def load_model():
    global _model
    _model = joblib.load(Path(__file__).resolve().parent.parent / "houseprice.joblib")

def is_loaded():
    return _model is not None

def predict_price(features: dict) -> float:
    """Take a dict of feature values and return the predicted price."""
    if _model is None:
        raise RuntimeError("Model is not loaded")

    row = [[features[name] for name in FEATURES]]
    X = pd.DataFrame(row, columns=FEATURES)   # keeps column names, avoids sklearn warnings

    price = float(_model.predict(X)[0])
    return round(max(price, 0.0), 2)  