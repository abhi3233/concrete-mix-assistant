# 🏗️ Intelligent Concrete Mix Design Assistant (IS 456:2000 & ML Powered)

An end-to-end Machine Learning web application designed for civil engineers, site contractors, and concrete technologists. Built in compliance with **IS 456:2000 Table 5** standards and trained on the **UCI Concrete Compressive Strength Dataset**.

---

## 🔬 Comprehensive Process & Workflow Architecture

```
                               ┌────────────────────────────────────────┐
                               │   UCI Concrete Compressive Strength    │
                               │        Dataset (1030 Samples)          │
                               └───────────────────┬────────────────────┘
                                                   │
                                                   ▼
                               ┌────────────────────────────────────────┐
                               │      Reproducible 80/20 Split          │
                               │          (random_state=42)             │
                               └───────────────────┬────────────────────┘
                                                   │
                                                   ▼
                               ┌────────────────────────────────────────┐
                               │       XGBoost Regressor Model          │
                               │   (Test R² = 0.9141, RMSE = 4.71 MPa)  │
                               └───────────────────┬────────────────────┘
                                                   │
                                                   ▼
 ┌───────────────────────────┐   ┌──────────────────────────────────────┐
 │  User Mix Inputs (kg/m³)  │──►│ 28-Day Curing Rule Lock (age = 28.0) │
 └───────────────────────────┘   └───────────────────┬──────────────────┘
                                                     │
                                                     ▼
                                 ┌──────────────────────────────────────┐
                                 │   ML 28-Day Compressive Strength     │
                                 │       Prediction Engine (MPa)        │
                                 └───────────────────┬──────────────────┘
                                                     │
                                                     ▼
 ┌───────────────────────────┐   ┌──────────────────────────────────────┐
 │  IS 456 Table 5 Standards │──►│ Dual Independent Status Dashboard    │
 │ (Min Cement & Max W/C)    │   │ (Strength Pass/Fail & Code Pass/Fail)│
 └───────────────────────────┘   └───────────────────┬──────────────────┘
                                                     │
                                                     ▼
                                 ┌──────────────────────────────────────┐
                                 │   Intelligent Recommendation Engine  │
                                 │ (Directional Deltas & Re-simulation) │
                                 └──────────────────────────────────────┘
```

### Step 1: Data Acquisition & Model Training Pipeline
1. **Dataset Ingestion**: Automatically fetches and parses the official UCI Concrete Compressive Strength dataset (1030 samples, 8 input features, 1 target variable).
2. **Reproducible Split**: Splits dataset into 80% training (824 samples) and 20% held-out test evaluation (206 samples) with a fixed random seed (`random_state=42`).
3. **Algorithm Benchmarking**: Compares Random Forest, Gradient Boosting, and XGBoost. XGBoost achieved top performance:
   - **Test $R^2$ Score**: `0.9141`
   - **Test RMSE**: `4.7051 MPa`
4. **28-Day Inference Locking**: The model is trained on multi-age samples (1 to 365 days) to learn age-dependent hydration kinetics. However, for all live web app predictions, curing age is **locked strictly at `age = 28.0` days** to adhere to IS 456 characteristic strength standards.

### Step 2: IS 456:2000 Civil Engineering Logic Layer
1. **Grade Standard Mapping**: Maps predicted 28-day strength into standard Indian Standard concrete grades:
   - $< 20 \text{ MPa} \implies \text{Below-grade (< M20)}$
   - $20 \le \text{Strength} < 25 \implies \text{M20}$
   - $25 \le \text{Strength} < 30 \implies \text{M25}$
   - $30 \le \text{Strength} < 35 \implies \text{M30}$
   - $35 \le \text{Strength} < 40 \implies \text{M35}$
   - $\ge 40 \text{ MPa} \implies \text{M40 and above (M40+)}$

2. **Independent Table 5 Compliance Verification**:
   - Checks minimum cement content and maximum Water-Cement ratio for user-specified target grades:
     - **M20**: Min Cement $300 \text{ kg/m}^3$, Max W/C $0.55$, Min Strength $20 \text{ MPa}$
     - **M25**: Min Cement $300 \text{ kg/m}^3$, Max W/C $0.50$, Min Strength $25 \text{ MPa}$
     - **M30**: Min Cement $320 \text{ kg/m}^3$, Max W/C $0.45$, Min Strength $30 \text{ MPa}$
     - **M35**: Min Cement $340 \text{ kg/m}^3$, Max W/C $0.45$, Min Strength $35 \text{ MPa}$
     - **M40**: Min Cement $360 \text{ kg/m}^3$, Max W/C $0.40$, Min Strength $40 \text{ MPa}$
   - **W/C Ratio Calculation Rule**: Calculated strictly as $\text{Water} \div \text{Cement}$ per IS 456 Table 5 instructions (Fly ash and Slag do NOT count toward the denominator).

3. **Dual Status Dashboard**: Separates compressive strength status (`STRENGTH PASS` / `STRENGTH FAIL`) from code compliance status (`CODE PASS` / `CODE FAIL`). This ensures site engineers can immediately see whether a mix fails due to durability risk (e.g. low cement or high water) vs structural strength shortfall.

### Step 3: Directional Recommendation & Simulation Verification Engine
When a mix fails strength OR compliance requirements:
1. **Root Cause Analysis**: Identifies whether failure is caused by low cement content, excessive water, or general strength shortfall.
2. **Feature Leverage Calculation**: Uses model feature importances (Cement, Water, Superplasticizer) to specify **directional adjustments with exact quantity deltas ($\pm \text{kg/m}^3$)**.
3. **Simulation Verification**: Automatically re-predicts compressive strength and re-verifies IS 456 compliance for the adjusted mix.
4. **1-Click Interactive Apply**: Allows users/evaluators to click **"✨ Apply Recommended Mix Proportions"** to load the corrected values into the input form.

### Step 4: Real-time Density & Weight Monitoring
- Continuously sums all constituent weights per $\text{m}^3$ ($\text{Target} \approx 2400 \text{ kg/m}^3$).
- Alerts user if total mix weight deviates from standard structural concrete density ($2200 - 2600 \text{ kg/m}^3$).

---

## 🎯 Key Features Overview

1. **28-Day Compressive Strength Prediction**:
   - Machine Learning model trained on 1030 UCI concrete samples (80/20 train/test split, `random_state=42`).
   - Inference strictly enforces **fixed 28-day curing age** (`age = 28.0`).
   - Reports test set **RMSE** and **$R^2$** metrics dynamically in the UI.

2. **IS 456:2000 Civil Engineering Logic Layer**:
   - **Grade Mapping**: Automatically maps predicted strength to standard Indian Standard grades.
   - **Independent Compliance Checking**: Evaluates target grade requirements independently of predicted strength.
   - **Dual Dashboard**: Clear, distinct status cards separating Strength Pass/Fail from Code Compliance Pass/Fail.

3. **Intelligent Recommendation Engine**:
   - Specifies directional, ingredient-specific quantity deltas (in $\text{kg/m}^3$).
   - Re-predicts strength and re-evaluates compliance on the adjusted mix.

4. **Real-time Density Monitor**:
   - Continuously sums total constituent weight ($\approx 2400 \text{ kg/m}^3$) and alerts users if mix density strays from structural norms.

---

## 🛠️ Installation & Local Setup

### 1. Clone Repository & Install Dependencies
```bash
git clone https://github.com/abhi3233/concrete-mix-assistant.git
cd concrete-mix-assistant
pip install -r requirements.txt
```

### 2. Train Model & Evaluate
```bash
python train_model.py
```
*Downloads UCI dataset, splits 80/20 with `random_state=42`, evaluates XGBoost/RandomForest, and saves `model_assets.joblib`.*

### 3. Run Streamlit Application
```bash
streamlit run app.py
```
Open browser at `http://localhost:8501`.

### 4. Run Automated Unit Tests
```bash
pytest test_app.py
```

---

## 🤗 Deploying to Hugging Face Spaces

1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces).
2. Select **Streamlit** as the Space SDK.
3. Push all files (`app.py`, `is456_logic.py`, `ml_engine.py`, `recommender.py`, `train_model.py`, `requirements.txt`, `model_assets.joblib`) to your HF Space repo.
4. Hugging Face will automatically install dependencies and launch the app at a public URL.

---

## 📄 IS 456:2000 Table 5 Quick Reference

| Grade | Min. Strength (MPa) | Min. Cement ($\text{kg/m}^3$) | Max. W/C Ratio ($\text{Water} \div \text{Cement}$) |
| :--- | :---: | :---: | :---: |
| **M20** | 20 | 300 | 0.55 |
| **M25** | 25 | 300 | 0.50 |
| **M30** | 30 | 320 | 0.45 |
| **M35** | 35 | 340 | 0.45 |
| **M40** | 40 | 360 | 0.40 |
