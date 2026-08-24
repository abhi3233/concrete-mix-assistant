"""
Unit Test Suite for Concrete Mix Design Assistant
Tests IS 456 logic, ML engine, 28-day age constraint, and recommendation verification.
"""

import pytest
from is456_logic import classify_grade, calculate_wc_ratio, check_is456_compliance, check_mix_weight
from ml_engine import predict_28day_strength, get_model_metrics
from recommender import generate_recommendation

def test_grade_classification():
    assert classify_grade(15.0) == "Below-grade (< M20)"
    assert classify_grade(22.5) == "M20"
    assert classify_grade(27.0) == "M25"
    assert classify_grade(32.0) == "M30"
    assert classify_grade(37.5) == "M35"
    assert classify_grade(42.0) == "M40 and above (M40+)"

def test_wc_ratio_calculation():
    assert calculate_wc_ratio(150.0, 300.0) == 0.50
    assert calculate_wc_ratio(180.0, 300.0) == 0.60
    assert calculate_wc_ratio(100.0, 0.0) == float('inf')

def test_is456_compliance_m30():
    # Target M30 requires: Min Strength 30 MPa, Min Cement 320 kg/m3, Max W/C 0.45
    
    # Passing mix
    pass_res = check_is456_compliance(cement=350.0, water=150.0, target_grade="M30")
    assert pass_res["is_compliant"] is True
    assert pass_res["cement_pass"] is True
    assert pass_res["wc_pass"] is True

    # Failing Cement mix
    fail_c = check_is456_compliance(cement=280.0, water=120.0, target_grade="M30")
    assert fail_c["is_compliant"] is False
    assert fail_c["cement_pass"] is False
    assert len(fail_c["reasons"]) > 0

    # Failing W/C mix
    fail_wc = check_is456_compliance(cement=350.0, water=180.0, target_grade="M30")
    assert fail_wc["is_compliant"] is False
    assert fail_wc["wc_pass"] is False
    assert fail_wc["wc_actual"] == pytest.approx(0.514, rel=1e-2)

def test_mix_weight_check():
    sample_mix = {
        "cement": 350.0, "blast_furnace_slag": 0.0, "fly_ash": 0.0,
        "water": 155.0, "superplasticizer": 6.0, "coarse_aggregate": 1050.0, "fine_aggregate": 840.0
    }
    res = check_mix_weight(sample_mix)
    assert res["total_weight"] == 2401.0
    assert res["is_optimal"] is True

def test_ml_engine_prediction():
    sample_mix = {
        "cement": 350.0, "blast_furnace_slag": 0.0, "fly_ash": 0.0,
        "water": 155.0, "superplasticizer": 6.0, "coarse_aggregate": 1050.0, "fine_aggregate": 840.0
    }
    strength = predict_28day_strength(sample_mix)
    assert isinstance(strength, float)
    assert strength > 0.0

def test_ml_model_metrics():
    rmse, r2, model_name, importances = get_model_metrics()
    assert rmse > 0.0
    assert r2 > 0.5
    assert isinstance(model_name, str)
    assert "cement" in importances

def test_recommender_low_cement_compliance_failure():
    # Mix with cement 250 kg/m3 (below M30 min cement 320 kg/m3)
    mix = {
        "cement": 250.0, "blast_furnace_slag": 0.0, "fly_ash": 0.0,
        "water": 120.0, "superplasticizer": 0.0, "coarse_aggregate": 1100.0, "fine_aggregate": 900.0
    }
    pred_s = predict_28day_strength(mix)
    rec = generate_recommendation(mix, target_grade="M30", predicted_strength=pred_s)

    assert rec["needs_adjustment"] is True
    assert rec["adjusted_mix"]["cement"] >= 320.0
    assert rec["adjusted_compliance"]["is_compliant"] is True

def test_recommender_strength_shortfall():
    # Weak mix for M40 target
    mix = {
        "cement": 300.0, "blast_furnace_slag": 0.0, "fly_ash": 0.0,
        "water": 180.0, "superplasticizer": 0.0, "coarse_aggregate": 1000.0, "fine_aggregate": 900.0
    }
    pred_s = predict_28day_strength(mix)
    rec = generate_recommendation(mix, target_grade="M40", predicted_strength=pred_s)

    assert rec["needs_adjustment"] is True
    assert rec["adjusted_strength"] > pred_s
    assert rec["adjusted_strength"] >= 40.0
