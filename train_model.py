"""
Training Script for UCI Concrete Compressive Strength Dataset
Downloads dataset, cleans headers, splits train/test (80/20, seed=42),
trains & compares regression models, saves best model and evaluation metrics.
"""

import os
import io
import urllib.request
import zipfile
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor

DATA_URL = "https://archive.ics.uci.edu/static/public/165/concrete+compressive+strength.zip"
CACHE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(CACHE_DIR, "Concrete_Data.xls")
MODEL_PATH = os.path.join(CACHE_DIR, "model_assets.joblib")

FEATURE_MAPPING = {
    "Cement": "cement",
    "Blast Furnace Slag": "blast_furnace_slag",
    "Fly Ash": "fly_ash",
    "Water": "water",
    "Superplasticizer": "superplasticizer",
    "Coarse Aggregate": "coarse_aggregate",
    "Fine Aggregate": "fine_aggregate",
    "Age": "age",
}

FEATURE_COLS = [
    "cement",
    "blast_furnace_slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
    "age"
]

TARGET_COL = "compressive_strength"

def fetch_dataset() -> pd.DataFrame:
    """Downloads and loads the UCI Concrete dataset."""
    if not os.path.exists(DATASET_PATH):
        print(f"Downloading dataset from {DATA_URL}...")
        zip_path = os.path.join(CACHE_DIR, "concrete.zip")
        urllib.request.urlretrieve(DATA_URL, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(CACHE_DIR)
        print("Dataset downloaded and extracted successfully.")

    # Load Excel file
    try:
        df = pd.read_excel(DATASET_PATH)
    except Exception:
        # Fallback search for any xls/xlsx file extracted
        excel_files = [f for f in os.listdir(CACHE_DIR) if f.endswith('.xls') or f.endswith('.xlsx')]
        if excel_files:
            df = pd.read_excel(os.path.join(CACHE_DIR, excel_files[0]))
        else:
            raise FileNotFoundError("Could not locate Excel file in extracted archive.")

    # Clean column names
    clean_cols = []
    for col in df.columns:
        c_str = str(col).strip()
        matched = False
        for k, v in FEATURE_MAPPING.items():
            if k.lower() in c_str.lower():
                clean_cols.append(v)
                matched = True
                break
        if not matched:
            if "strength" in c_str.lower():
                clean_cols.append(TARGET_COL)
            else:
                clean_cols.append(c_str.lower().replace(" ", "_"))

    df.columns = clean_cols
    print("Cleaned Dataset Columns:", df.columns.tolist())
    print("Dataset Shape:", df.shape)
    return df

def train_and_evaluate():
    df = fetch_dataset()

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    # Reproducible 80/20 train-test split with fixed random state 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")

    candidate_models = {
        "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, random_state=42),
        "XGBoost": XGBRegressor(n_estimators=200, learning_rate=0.08, max_depth=6, random_state=42, n_jobs=-1)
    }

    best_name = None
    best_model = None
    best_r2 = -1.0
    best_rmse = 999.0
    results = {}

    for name, model in candidate_models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        results[name] = {"rmse": rmse, "r2": r2}
        print(f"Model: {name:<18} | Test RMSE: {rmse:.4f} MPa | Test R2: {r2:.4f}")

        if r2 > best_r2:
            best_r2 = r2
            best_rmse = rmse
            best_model = model
            best_name = name

    print(f"\nBest Performing Model: {best_name} (R2 = {best_r2:.4f}, RMSE = {best_rmse:.4f} MPa)")

    # Extract Feature Importances
    importances = dict(zip(FEATURE_COLS, best_model.feature_importances_))

    artifacts = {
        "model": best_model,
        "model_name": best_name,
        "feature_cols": FEATURE_COLS,
        "test_rmse": float(best_rmse),
        "test_r2": float(best_r2),
        "all_results": results,
        "feature_importances": importances,
        "test_split_info": "80/20 train/test split, random_state=42, 1030 samples total"
    }

    joblib.dump(artifacts, MODEL_PATH)
    print(f"Saved trained model artifacts to {MODEL_PATH}")
    return artifacts

if __name__ == "__main__":
    train_and_evaluate()
