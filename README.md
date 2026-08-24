# 🏗️ Intelligent Concrete Mix Design Assistant (IS 456:2000 & ML Powered)

[![Live Web Application](https://img.shields.io/badge/Live_App-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit)](https://concrete-mix-assistant-gws95dtjpkxwrvwunuqcnt.streamlit.app/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/abhi3233/concrete-mix-assistant)
[![IS 456:2000 Compliant](https://img.shields.io/badge/Civil_Code-IS_456%3A2000-008080?style=for-the-badge)](https://github.com/abhi3233/concrete-mix-assistant)

An end-to-end Machine Learning web application designed for civil engineers, site contractors, and concrete technologists. Built in compliance with **IS 456:2000 Table 5** standards and trained on the **UCI Concrete Compressive Strength Dataset**.

---

## 🌐 Live Application URL & Deployment Overview

### 👉 **Live Web Application**: [https://concrete-mix-assistant-gws95dtjpkxwrvwunuqcnt.streamlit.app/](https://concrete-mix-assistant-gws95dtjpkxwrvwunuqcnt.streamlit.app/)

### 🚀 Basic Deployment Architecture:
- **Hosting Platform**: Streamlit Community Cloud (Global CDN).
- **Source Repository**: Continuous Deployment directly connected to `main` branch of [GitHub Repo](https://github.com/abhi3233/concrete-mix-assistant.git).
- **Public Access**: 100% free, publicly accessible with **no login required** for evaluators or field engineers.
- **Runtime Environment**: Containerized Python 3.13 environment running trained XGBoost ML inference, automated IS 456 logic, and real-time recommendation engine.

---

## 📖 First-Time Visitor Guide ("What is What" on Screen)

When a user or evaluator opens [https://concrete-mix-assistant-gws95dtjpkxwrvwunuqcnt.streamlit.app/](https://concrete-mix-assistant-gws95dtjpkxwrvwunuqcnt.streamlit.app/), here is a complete guide to every element displayed on screen:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🏗️ INTELLIGENT CONCRETE MIX DESIGN ASSISTANT (LIVE INTERFACE)                                  │
├─────────────────────────────────────┬───────────────────────────────────────────────────────────┤
│ ⚙️ LEFT SIDEBAR CONTROLS            │ 📐 MAIN DASHBOARD (INPUTS & LIVE ANALYSIS)                │
│                                     │                                                           │
│ 1️⃣ Target IS 456 Grade Selector     │ 4️⃣ Concrete Mix Proportions Input Form                    │
│    • Choose M20, M25, M30, M35, M40 │    • 7 constituent weight sliders/boxes (kg/m³)          │
│    • Displays Code Min/Max values   │    • Cement, Slag, Fly Ash, Water, Superplasticizer,   │
│                                     │      Coarse Aggregate, Fine Aggregate                    │
│ 2️⃣ ML Model Metrics                 │                                                           │
│    • Test RMSE: 4.71 MPa            │ 5️⃣ ⚖️ Total Mix Density Monitor                          │
│    • Test R²: 0.914                 │    • Sums total weight per m³ (Target ≈ 2400 kg/m³)      │
│    • Curing Age: 28 Days Locked     │                                                           │
│                                     │ 6️⃣ 🤖 ML Strength Prediction Card                        │
│ 3️⃣ 💡 Quick Test Presets            │    • Predicted Strength (MPa) & Mapped IS 456 Grade      │
│    • Standard M30 Mix               │    • STRENGTH PASS / STRENGTH FAIL Badge                  │
│    • Low Cement Violating Mix       │                                                           │
│    • High W/C Ratio Violating Mix   │ 7️⃣ 📜 IS 456:2000 Code Compliance Card                   │
│    • High Strength M40+ Mix         │    • Min Cement Check & Max W/C Ratio (Water ÷ Cement)    │
│                                     │    • CODE PASS / CODE FAIL Badge                          │
│                                     │                                                           │
│                                     │ 8️⃣ 💡 Intelligent Recommendation Engine                   │
│                                     │    • Directional Adjustments (± kg/m³)                    │
│                                     │    • Before vs After Verification Table                   │
│                                     │    • ✨ 1-Click "Apply Recommended Mix" Button            │
└─────────────────────────────────────┴───────────────────────────────────────────────────────────┘
```

### 1️⃣ Target IS 456 Grade Selector *(Left Sidebar)*
- **What it is**: A drop-down menu allowing you to select your target concrete grade (**M20, M25, M30, M35, or M40**).
- **What it does**: Dynamically loads code-mandated IS 456:2000 Table 5 requirements (Minimum 28-day strength, minimum cement content, and maximum allowable water-cement ratio).

### 2️⃣ ML Model Metrics Card *(Left Sidebar)*
- **What it is**: Live model performance indicator.
- **What it does**: Displays the trained XGBoost model's accuracy on the 206-sample test set (**$R^2 = 0.914$**, **$\text{RMSE} = 4.71 \text{ MPa}$**) and confirms that all inference calls strictly enforce a **28-day curing age (`age = 28.0`)**.

### 3️⃣ 💡 Quick Test Presets *(Left Sidebar)*
- **What it is**: 4 pre-configured mix formulations for instant testing.
- **What it does**: Clicking **"Apply Selected Preset"** loads edge-case mix proportions (e.g. *Low Cement Mix* or *High W/C Mix*) into the form so you can test how the app detects failures and recommends fixes.

### 4️⃣ 📐 7-Ingredient Mix Input Form *(Main Left Column)*
- **What it is**: Numerical input fields for $1 \text{ m}^3$ of fresh concrete.
- **What it does**: Accepts constituent weights ($\text{kg/m}^3$) for Cement, Blast Furnace Slag, Fly Ash, Water, Superplasticizer, Coarse Aggregate, and Fine Aggregate.

### 5️⃣ ⚖️ Real-time Total Mix Density Monitor *(Main Left Column)*
- **What it is**: Real-time mass summation gauge.
- **What it does**: Calculates total mix weight per $\text{m}^3$ ($\text{Target} \approx 2400 \text{ kg/m}^3$) and alerts you if density strays outside structural norms ($2200 - 2600 \text{ kg/m}^3$).

### 6️⃣ 🤖 ML Strength Prediction Card *(Main Right Column)*
- **What it is**: Machine Learning prediction output box.
- **What it does**: Displays predicted 28-day strength in MPa, mapped IS 456 grade (e.g. `M40+`), and a green **`STRENGTH PASS`** or red **`STRENGTH FAIL`** badge depending on whether predicted strength meets your selected target grade.

### 7️⃣ 📜 IS 456:2000 Code Compliance Card *(Main Right Column)*
- **What it is**: Independent civil engineering code compliance checker.
- **What it does**: Calculates W/C ratio as $\text{Water} \div \text{Cement}$ (excluding fly ash and slag per IS 456 Table 5), checks minimum cement requirements, and displays an independent green **`CODE PASS`** or red **`CODE FAIL`** badge.

### 8️⃣ 💡 Intelligent Recommendation Engine *(Main Bottom Panel)*
- **What it is**: Automated optimization and re-simulation panel.
- **What it does**: Triggers whenever a mix fails strength OR compliance. It provides exact directional adjustments ($\pm \text{kg/m}^3$), displays a **Before vs After verification table**, and provides a **"✨ Apply Recommended Mix Proportions"** button to load the verified mix into the form.

---

## 🛠️ Comprehensive Technology Stack & Architecture Details

| Layer / Category | Technology / Library | Version | Purpose & Technical Role |
| :--- | :--- | :---: | :--- |
| **Language** | **Python** | `3.10+ / 3.13` | Core runtime environment for data science, ML pipeline, and application logic. |
| **Machine Learning** | **XGBoost Regressor** | `^3.4.1` | **Primary Predictive Model**: Selected for superior non-linear performance ($R^2 = \mathbf{0.9141}$, $\text{RMSE} = \mathbf{4.71 \text{ MPa}}$). |
| **Data Science & ML** | **Scikit-Learn** | `^1.9.0` | Dataset train/test splitting (`80/20, seed=42`), evaluation metrics (`r2_score`, `mean_squared_error`), and baseline benchmarks. |
| **Data Manipulation** | **Pandas** | `^3.0.5` | Tabular data cleaning, feature mapping, input dataframe construction, and mix vector transformations. |
| **Numerical Computing** | **NumPy** | `^2.0.0` | High-performance vectorized arithmetic, RMSE calculation, and statistical computations. |
| **Model Serialization** | **Joblib** | `^1.5.3` | Exporting and fast loading of trained model artifacts (`model_assets.joblib`), feature importances, and evaluation metadata. |
| **Web UI Framework** | **Streamlit** | `^1.62.0` | **Frontend Framework**: Reactive web dashboard, sidebar controls, session state management, and real-time input sliders. |
| **UI Styling** | **Vanilla CSS3 & HTML5** | Standard | Custom CSS styling for glassmorphism card layouts, status badges (`CODE PASS`, `STRENGTH FAIL`), and responsive typography. |
| **Data Acquisition** | **Urllib & Zipfile** | Standard Library | Automated fetching and extraction of the raw UCI Concrete Compressive Strength dataset. |
| **Excel Parsing** | **Xlrd & Openpyxl** | `^2.0.2` / `^3.1.5` | Parsing and loading binary Microsoft Excel files (`Concrete_Data.xls`). |
| **Automated Testing** | **Pytest** | `^9.1.1` | Unit test suite verifying IS 456 logic, grade mapping, 28-day age constraint, and recommendation re-simulation. |
| **Version Control** | **Git & GitHub** | Standard | Source code versioning and public repository hosting ([abhi3233/concrete-mix-assistant](https://github.com/abhi3233/concrete-mix-assistant.git)). |
| **Cloud Deployment** | **Streamlit Community Cloud** | Free Tier | Public web app hosting containerized with Streamlit runtime. |

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

## 📄 IS 456:2000 Table 5 Quick Reference

| Grade | Min. Strength (MPa) | Min. Cement ($\text{kg/m}^3$) | Max. W/C Ratio ($\text{Water} \div \text{Cement}$) |
| :--- | :---: | :---: | :---: |
| **M20** | 20 | 300 | 0.55 |
| **M25** | 25 | 300 | 0.50 |
| **M30** | 30 | 320 | 0.45 |
| **M35** | 35 | 340 | 0.45 |
| **M40** | 40 | 360 | 0.40 |
