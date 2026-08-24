# 🏗️ Intelligent Concrete Mix Design Assistant (IS 456:2000 & ML Powered)

An end-to-end Machine Learning web application designed for civil engineers, site contractors, and concrete technologists. Built in compliance with **IS 456:2000 Table 5** standards and trained on the **UCI Concrete Compressive Strength Dataset**.

---

## 🖥️ Interactive Dashboard & Features Guide (What You Can Do)

The application features a clean, responsive dual-column dashboard tailored for intuitive operation by both technical evaluators and field site engineers.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   MAIN APPLICATION DASHBOARD                                     │
├──────────────────────────────────────┬───────────────────────────────────────────────────────────┤
│ SIDEBAR CONTROLS                     │ MAIN CONTENT PANEL                                        │
│                                      │                                                           │
│ 📌 Target Grade Selector             │ 📐 Concrete Mix Inputs (7 Proportions)                   │
│    • M20, M25, M30, M35, M40         │    • Cement, Slag, Fly Ash, Water, Superplasticizer,   │
│    • Live IS 456 Table 5 Specs       │      Coarse Aggregate, Fine Aggregate                    │
│                                      │    • Real-time Total Density Monitor (≈ 2400 kg/m³)       │
│ 📊 ML Model Metrics                  │                                                           │
│    • Test RMSE: 4.71 MPa             │ 🔍 Dual Independent Status Cards                         │
│    • Test R²: 0.914                  │    • 🤖 ML Strength Prediction (MPa & Mapped Grade)       │
│    • Locked 28-Day Curing Rule       │    • 📜 IS 456 Code Compliance (Cement & W/C Ratio)      │
│                                      │                                                           │
│ 💡 Quick Test Presets                │ 💡 Intelligent Recommendation & Simulation               │
│    • Standard M30 Mix                │    • Directional Deltas (± kg/m³)                        │
│    • Low Cement Violating Mix        │    • Before vs After Verification Table                   │
│    • High W/C Ratio Violating Mix    │    • ✨ 1-Click "Apply Recommendation" Button            │
│    • High Strength M40+ Mix          │                                                           │
└──────────────────────────────────────┴───────────────────────────────────────────────────────────┘
```

### 1. 📌 Target Grade Selection & IS 456 Specification Card
- **What It Does**: Allows users to select any target concrete grade (**M20, M25, M30, M35, M40**).
- **What You Can Do**: Instantly view the code-mandated minimum 28-day compressive strength, minimum cement content, and maximum water-cement ratio required for structural compliance under IS 456:2000 Table 5.

### 2. 📊 Real-time ML Model Performance & Reproducibility Metrics
- **What It Does**: Displays test set **RMSE (`4.71 MPa`)** and test **$R^2$ score (`0.914`)** for the trained XGBoost model.
- **What You Can Do**: Verify model accuracy, inspect the 80/20 train/test split details (`random_state=42`, 1030 samples), and confirm the locked 28-day curing age inference rule (`age = 28.0`).

### 3. 💡 One-Click Quick Test Presets
- **What It Does**: Provides pre-configured mix formulations:
  - `Standard M30 Mix (Balanced)`
  - `Low Cement Mix (Violates IS 456)`
  - `High W/C Ratio Mix (Violates IS 456)`
  - `High Strength M40+ Mix`
- **What You Can Do**: Instantly load edge-case concrete mixes into the input form with 1 click to test how the app handles compliance violations, strength shortfalls, and recommendations.

### 4. 📐 7-Ingredient Mix Input Panel
- **What It Does**: Provides numerical inputs for Cement, Blast Furnace Slag, Fly Ash, Water, Superplasticizer, Coarse Aggregate, and Fine Aggregate (in $\text{kg/m}^3$).
- **What You Can Do**: Enter custom mix proportions for $1 \text{ m}^3$ of fresh concrete and observe instant real-time recalculations.

### 5. ⚖️ Real-time Total Mix Density Monitor
- **What It Does**: Continuously sums all constituent weights per $\text{m}^3$ ($\text{Target} \approx 2400 \text{ kg/m}^3$).
- **What You Can Do**: Monitor total mix mass and receive immediate warning alerts if a mix strays outside standard structural concrete density ($2200 - 2600 \text{ kg/m}^3$).

### 6. 🔍 Dual Independent Status Dashboard
- **What It Does**: Renders two decoupled status cards:
  - **🤖 ML Strength Prediction Card**: Displays predicted 28-day strength in MPa, mapped IS 456 grade (e.g. `M40+`), and a `STRENGTH PASS` or `STRENGTH FAIL` badge.
  - **📜 IS 456:2000 Compliance Card**: Independently checks Cement content vs minimum requirement and W/C ratio ($\text{Water} \div \text{Cement}$) vs maximum allowed ratio, displaying a `CODE PASS` or `CODE FAIL` badge.
- **What You Can Do**: Instantly distinguish between a structural strength failure and a durability/compliance code violation so you never have to guess why a mix failed.

### 7. 💡 Intelligent Recommendation Engine & Interactive Re-Simulation Panel
- **What It Does**: Triggers automatically whenever a mix fails strength OR code compliance. Identifies root causes and calculates directional adjustments with exact quantity deltas ($\pm \text{kg/m}^3$).
- **What You Can Do**:
  - View explicit step-by-step ingredient modifications (e.g., *"Increase Cement by +40.0 kg/m³"* or *"Decrease Water by -15.0 kg/m³"*).
  - Compare **Before vs After** strength predictions and compliance status in a side-by-side verification table.
  - Click **"✨ Apply Recommended Mix Proportions"** to automatically load the optimized, verified mix directly into the input form!

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
