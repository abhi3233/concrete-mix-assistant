"""
ML Engine Module
Provides clean wrapper functions for loading the ML model artifacts,
predicting 28-day compressive strength, and querying model evaluation metrics.
"""

import os
import joblib
import pandas as pd
from typing import Dict, Any, Tuple

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_assets.joblib")

_model_artifacts = None

def get_model_artifacts() -> Dict[str, Any]:
    """Loads and caches model artifacts. Trains model on the fly if joblib missing."""
    global _model_artifacts
    if _model_artifacts is None:
        if not os.path.exists(MODEL_PATH):
            from train_model import train_and_evaluate
            _model_artifacts = train_and_evaluate()
        else:
            _model_artifacts = joblib.load(MODEL_PATH)
    return _model_artifacts

def predict_28day_strength(ingredients: Dict[str, float]) -> float:
    """
    Predicts 28-day compressive strength (MPa) for given 7 mix proportions.
    Enforces age = 28.0 days as specified by Problem Requirements.
    """
    artifacts = get_model_artifacts()
    model = artifacts["model"]
    feature_cols = artifacts["feature_cols"]

    # Construct feature row with age explicitly locked to 28 days
    input_data = {
        "cement": float(ingredients.get("cement", 0.0)),
        "blast_furnace_slag": float(ingredients.get("blast_furnace_slag", 0.0)),
        "fly_ash": float(ingredients.get("fly_ash", 0.0)),
        "water": float(ingredients.get("water", 0.0)),
        "superplasticizer": float(ingredients.get("superplasticizer", 0.0)),
        "coarse_aggregate": float(ingredients.get("coarse_aggregate", 0.0)),
        "fine_aggregate": float(ingredients.get("fine_aggregate", 0.0)),
        "age": 28.0  # ALWAYS LOCKED TO 28 DAYS FOR APP PREDICTIONS
    }

    df_input = pd.DataFrame([input_data])[feature_cols]
    prediction = float(model.predict(df_input)[0])
    return max(0.0, prediction)

def get_model_metrics() -> Tuple[float, float, str, Dict[str, float]]:
    """Returns (rmse, r2, model_name, feature_importances)."""
    artifacts = get_model_artifacts()
    return (
        artifacts.get("test_rmse", 0.0),
        artifacts.get("test_r2", 0.0),
        artifacts.get("model_name", "Unknown"),
        artifacts.get("feature_importances", {})
    )
