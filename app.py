"""
Intelligent Concrete Mix Design Assistant (Streamlit Web Application)
Compliant with IS 456:2000 & ML Powered (UCI Dataset Trained).
"""

import streamlit as st
import pandas as pd
import numpy as np
from is456_logic import IS456_SPECS, AVAILABLE_GRADES, classify_grade, check_is456_compliance, check_mix_weight, calculate_wc_ratio
from ml_engine import predict_28day_strength, get_model_metrics
from recommender import generate_recommendation

# Page Configuration
st.set_page_config(
    page_title="Concrete Mix Design Assistant | IS 456:2000",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .status-pass {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 700;
        display: inline-block;
    }
    .status-fail {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 700;
        display: inline-block;
    }
    .rec-box {
        background-color: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 1rem;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Preset Mix Configurations for testing
PRESETS = {
    "Standard M30 Mix (Balanced)": {
        "cement": 350.0, "blast_furnace_slag": 0.0, "fly_ash": 0.0,
        "water": 155.0, "superplasticizer": 6.0, "coarse_aggregate": 1050.0, "fine_aggregate": 840.0
    },
    "Low Cement Mix (Violates IS 456)": {
        "cement": 260.0, "blast_furnace_slag": 50.0, "fly_ash": 0.0,
        "water": 170.0, "superplasticizer": 0.0, "coarse_aggregate": 1080.0, "fine_aggregate": 840.0
    },
    "High W/C Ratio Mix (Violates IS 456)": {
        "cement": 310.0, "blast_furnace_slag": 0.0, "fly_ash": 0.0,
        "water": 190.0, "superplasticizer": 0.0, "coarse_aggregate": 1020.0, "fine_aggregate": 880.0
    },
    "High Strength M40+ Mix": {
        "cement": 420.0, "blast_furnace_slag": 80.0, "fly_ash": 0.0,
        "water": 150.0, "superplasticizer": 10.0, "coarse_aggregate": 1000.0, "fine_aggregate": 750.0
    }
}

def main():
    # Header Banner
    st.markdown('<div class="main-header">🏗️ Intelligent Concrete Mix Design Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">28-Day ML Compressive Strength Prediction & IS 456:2000 Structural Compliance Engine</div>', unsafe_allow_html=True)

    # Initialize Session State for ingredients
    if "mix_inputs" not in st.session_state:
        st.session_state.mix_inputs = PRESETS["Standard M30 Mix (Balanced)"].copy()

    # Sidebar: Project Info, Model Metrics & Presets
    with st.sidebar:
        st.header("⚙️ Settings & Model Metrics")

        target_grade = st.selectbox("Target IS 456 Grade", AVAILABLE_GRADES, index=2)
        st.markdown(f"""
        **Selected Grade Target ({target_grade}) Requirements:**
        - **Min 28-Day Strength**: `{IS456_SPECS[target_grade]['min_strength']} MPa`
        - **Min Cement Content**: `{IS456_SPECS[target_grade]['min_cement']} kg/m³`
        - **Max W/C Ratio**: `{IS456_SPECS[target_grade]['max_wc']}`
        """)
        st.divider()

        # Fetch and Display ML Model Metrics
        try:
            rmse, r2, model_name, importances = get_model_metrics()
            st.subheader("📊 ML Model Evaluation")
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Test RMSE", f"{rmse:.2f} MPa")
            col_m2.metric("Test R² Score", f"{r2:.3f}")
            st.caption(f"**Algorithm**: `{model_name}` trained on UCI Dataset (1030 samples, 80/20 split, seed=42).")
            st.caption("🔒 **Inference Rule**: All predictions locked at **28 days age**.")
        except Exception as e:
            st.error(f"Error loading model metrics: {e}")

        st.divider()
        st.subheader("💡 Load Test Presets")
        selected_preset = st.selectbox("Quick Preset Mixes", list(PRESETS.keys()))
        if st.button("Apply Selected Preset"):
            st.session_state.mix_inputs = PRESETS[selected_preset].copy()
            st.rerun()

    # Main Layout: 2 Columns (Inputs vs Analysis)
    col_input, col_output = st.columns([1.1, 1.3], gap="large")

    with col_input:
        st.subheader("📐 Concrete Mix Proportions (kg/m³)")
        st.caption("Enter constituent weights for 1 m³ of fresh concrete mix.")

        c_val = st.number_input("Cement (kg/m³)", min_value=0.0, max_value=800.0, value=float(st.session_state.mix_inputs["cement"]), step=10.0)
        slag_val = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, max_value=500.0, value=float(st.session_state.mix_inputs["blast_furnace_slag"]), step=10.0)
        fa_val = st.number_input("Fly Ash (kg/m³)", min_value=0.0, max_value=400.0, value=float(st.session_state.mix_inputs["fly_ash"]), step=10.0)
        w_val = st.number_input("Water (kg/m³)", min_value=0.0, max_value=350.0, value=float(st.session_state.mix_inputs["water"]), step=5.0)
        sp_val = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, max_value=35.0, value=float(st.session_state.mix_inputs["superplasticizer"]), step=0.5)
        ca_val = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, max_value=1500.0, value=float(st.session_state.mix_inputs["coarse_aggregate"]), step=20.0)
        fine_val = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, max_value=1200.0, value=float(st.session_state.mix_inputs["fine_aggregate"]), step=20.0)

        current_mix = {
            "cement": c_val,
            "blast_furnace_slag": slag_val,
            "fly_ash": fa_val,
            "water": w_val,
            "superplasticizer": sp_val,
            "coarse_aggregate": ca_val,
            "fine_aggregate": fine_val
        }
        st.session_state.mix_inputs = current_mix

        # Real-time Mix Weight Monitor (~2400 kg/m³)
        weight_info = check_mix_weight(current_mix)
        st.divider()
        st.markdown(f"**⚖️ Total Mix Density**: `{weight_info['total_weight']:.1f} kg/m³` (Target ≈ 2400 kg/m³)")
        if weight_info['is_optimal']:
            st.success("✅ Mix density is within normal structural range (2200 - 2600 kg/m³).")
        else:
            st.warning(f"⚠️ Mix weight deviates from standard range ({weight_info['total_weight']:.1f} kg/m³). Consider adjusting aggregates.")

    with col_output:
        st.subheader("🔍 Mix Analysis & IS 456 Verification")

        # Run Prediction & IS 456 Compliance
        try:
            pred_strength = predict_28day_strength(current_mix)
            mapped_grade = classify_grade(pred_strength)
            is456_status = check_is456_compliance(c_val, w_val, target_grade)
            wc_actual = calculate_wc_ratio(w_val, c_val)
            min_req_strength = IS456_SPECS[target_grade]["min_strength"]

            strength_pass = pred_strength >= min_req_strength
            compliance_pass = is456_status["is_compliant"]

            # Display Dual Metric Cards
            card_col1, card_col2 = st.columns(2)

            with card_col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown("#### 🤖 ML Strength Prediction")
                st.markdown(f"## {pred_strength:.2f} <span style='font-size:1rem'>MPa</span>", unsafe_allow_html=True)
                st.markdown(f"**Mapped IS 456 Grade**: `{mapped_grade}`")
                if strength_pass:
                    st.markdown('<span class="status-pass">✅ STRENGTH PASS</span>', unsafe_allow_html=True)
                    st.caption(f"Meets target {target_grade} requirement ({min_req_strength} MPa).")
                else:
                    st.markdown('<span class="status-fail">❌ STRENGTH FAIL</span>', unsafe_allow_html=True)
                    st.caption(f"Below target {target_grade} requirement ({min_req_strength} MPa).")
                st.markdown('</div>', unsafe_allow_html=True)

            with card_col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown("#### 📜 IS 456:2000 Compliance")
                if compliance_pass:
                    st.markdown("## COMPLIANT", unsafe_allow_html=True)
                    st.markdown('<span class="status-pass">✅ CODE PASS</span>', unsafe_allow_html=True)
                else:
                    st.markdown("## VIOLATION", unsafe_allow_html=True)
                    st.markdown('<span class="status-fail">❌ CODE FAIL</span>', unsafe_allow_html=True)

                st.markdown(f"• **Cement**: `{c_val:.1f}` vs min `{is456_status['min_cement_required']:.0f}` kg/m³ " + ("✅" if is456_status['cement_pass'] else "❌"))
                st.markdown(f"• **W/C Ratio**: `{wc_actual:.3f}` vs max `{is456_status['max_wc_allowed']:.2f}` " + ("✅" if is456_status['wc_pass'] else "❌"))
                st.markdown('</div>', unsafe_allow_html=True)

            st.divider()

            # Recommendation Engine Section
            rec_result = generate_recommendation(current_mix, target_grade, pred_strength)

            if not rec_result["needs_adjustment"]:
                st.success("🎉 **Perfect Mix!** This concrete mix satisfies both predicted compressive strength targets and IS 456 code compliance constraints.")
            else:
                st.subheader("💡 Intelligent Recommendation Engine")
                st.warning(f"**Action Required**: Mix needs optimization due to **{rec_result['status']}**.")

                for rec in rec_result["recommendations"]:
                    st.markdown(f"- {rec}")

                st.markdown("#### 🔄 Re-prediction & Simulation Verification")
                col_ver1, col_ver2 = st.columns(2)
                with col_ver1:
                    st.markdown(f"**Original 28-Day Strength**: `{rec_result['original_strength']:.2f} MPa`")
                    st.markdown(f"**Original Compliance**: `{'PASS' if rec_result['initial_compliance']['is_compliant'] else 'FAIL'}`")
                with col_ver2:
                    st.markdown(f"**Adjusted 28-Day Strength**: `{rec_result['adjusted_strength']:.2f} MPa`")
                    st.markdown(f"**Adjusted Compliance**: `{'PASS' if rec_result['adjusted_compliance']['is_compliant'] else 'FAIL'}`")

                if st.button("✨ Apply Recommended Mix Proportions"):
                    st.session_state.mix_inputs = rec_result["adjusted_mix"].copy()
                    st.rerun()

        except Exception as e:
            st.error(f"Error during analysis: {e}")
            st.exception(e)

if __name__ == "__main__":
    main()
