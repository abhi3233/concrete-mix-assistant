"""
Recommendation Engine Module
Generates directional, ingredient-specific adjustments with exact quantity deltas
based on model feature importances and IS 456:2000 constraints.
Verifies suggestions by re-predicting strength and checking compliance.
"""

from typing import Dict, Any, List
from is456_logic import IS456_SPECS, check_is456_compliance, check_mix_weight, calculate_wc_ratio
from ml_engine import predict_28day_strength, get_model_metrics

def generate_recommendation(
    ingredients: Dict[str, float],
    target_grade: str,
    predicted_strength: float
) -> Dict[str, Any]:
    """
    Generates actionable ingredient adjustments when mix falls short of target strength or IS 456 constraints.
    Re-runs prediction to verify adjusted mix strength and compliance.
    """
    if target_grade not in IS456_SPECS:
        raise ValueError(f"Unknown grade: {target_grade}")

    spec = IS456_SPECS[target_grade]
    min_strength = spec["min_strength"]
    min_cement = spec["min_cement"]
    max_wc = spec["max_wc"]

    # Initial compliance check
    cement = float(ingredients.get("cement", 0.0))
    water = float(ingredients.get("water", 0.0))
    initial_compliance = check_is456_compliance(cement, water, target_grade)

    strength_pass = predicted_strength >= min_strength
    compliance_pass = initial_compliance["is_compliant"]

    if strength_pass and compliance_pass:
        return {
            "needs_adjustment": False,
            "status": "OPTIMAL",
            "message": f"Mix fully complies with IS 456 requirements and satisfies target strength ({predicted_strength:.2f} MPa ≥ {min_strength} MPa for {target_grade}).",
            "recommendations": [],
            "adjusted_mix": ingredients.copy(),
            "original_strength": predicted_strength,
            "adjusted_strength": predicted_strength,
            "initial_compliance": initial_compliance,
            "adjusted_compliance": initial_compliance
        }

    # Clone mix for adjustments
    adj_mix = ingredients.copy()
    rec_steps: List[str] = []
    reasons: List[str] = []

    # 1. Address IS 456 Compliance Violations First
    if not compliance_pass:
        reasons.append("IS 456 Compliance Violation")

        # Check cement content
        if cement < min_cement:
            delta_c = min_cement - cement
            adj_mix["cement"] = min_cement
            rec_steps.append(f"Increase **Cement** by **+{delta_c:.1f} kg/m³** (from {cement:.1f} to minimum {min_cement:.1f} kg/m³ to satisfy IS 456 Table 5).")

        # Check W/C ratio
        cur_c = adj_mix["cement"]
        cur_w = adj_mix["water"]
        wc_ratio = calculate_wc_ratio(cur_w, cur_c)

        if wc_ratio > max_wc:
            # Water reduction target
            max_water_allowed = cur_c * max_wc
            delta_w = cur_w - max_water_allowed
            if delta_w > 0:
                adj_mix["water"] = max_water_allowed
                rec_steps.append(f"Decrease **Water** by **-{delta_w:.1f} kg/m³** (from {cur_w:.1f} to {max_water_allowed:.1f} kg/m³ to achieve W/C ratio ≤ {max_wc:.2f}).")
                # Add superplasticizer if water reduced significantly and superplasticizer is low
                sp = float(adj_mix.get("superplasticizer", 0.0))
                if sp < 5.0:
                    add_sp = min(4.0, 8.0 - sp)
                    adj_mix["superplasticizer"] = sp + add_sp
                    rec_steps.append(f"Add **Superplasticizer** by **+{add_sp:.1f} kg/m³** to maintain workability after water reduction.")

    # 2. Re-evaluate strength on current adjustments
    re_pred = predict_28day_strength(adj_mix)

    # 3. Address Strength Shortfall if still below target
    if re_pred < min_strength:
        reasons.append("Strength Shortfall")
        shortfall = min_strength - re_pred

        # Feature leverage analysis: Cement & Superplasticizer are top leverage for strength
        # Iteratively optimize mix until target strength reached
        max_iters = 20
        step_c = 15.0  # kg/m3 cement step
        step_sp = 1.0  # kg/m3 superplasticizer step

        for _ in range(max_iters):
            if re_pred >= min_strength:
                break

            # Increase cement while respecting W/C constraint
            adj_mix["cement"] += step_c

            # Maintain water or slightly adjust water to keep W/C ratio compliant
            current_wc = calculate_wc_ratio(adj_mix["water"], adj_mix["cement"])
            if current_wc > max_wc:
                adj_mix["water"] = adj_mix["cement"] * max_wc

            # Add superplasticizer if strength shortfall persists
            if adj_mix["superplasticizer"] < 12.0:
                adj_mix["superplasticizer"] += step_sp

            re_pred = predict_28day_strength(adj_mix)

        # Summarize strength adjustment deltas relative to mix before strength adjustment
        cement_delta = adj_mix["cement"] - ingredients["cement"]
        water_delta = adj_mix["water"] - ingredients["water"]
        sp_delta = adj_mix["superplasticizer"] - ingredients["superplasticizer"]

        # Re-build recommendation list cleanly
        rec_steps = []
        if cement_delta != 0:
            direction = "Increase" if cement_delta > 0 else "Decrease"
            rec_steps.append(f"{direction} **Cement** by **{cement_delta:+.1f} kg/m³** (from {ingredients['cement']:.1f} to {adj_mix['cement']:.1f} kg/m³).")
        if water_delta != 0:
            direction = "Increase" if water_delta > 0 else "Decrease"
            rec_steps.append(f"{direction} **Water** by **{water_delta:+.1f} kg/m³** (from {ingredients['water']:.1f} to {adj_mix['water']:.1f} kg/m³).")
        if sp_delta != 0:
            direction = "Increase" if sp_delta > 0 else "Decrease"
            rec_steps.append(f"{direction} **Superplasticizer** by **{sp_delta:+.1f} kg/m³** (from {ingredients['superplasticizer']:.1f} to {adj_mix['superplasticizer']:.1f} kg/m³).")

    # Final Verification
    final_strength = predict_28day_strength(adj_mix)
    final_compliance = check_is456_compliance(adj_mix["cement"], adj_mix["water"], target_grade)

    status_str = " & ".join(reasons) if reasons else "Adjustment Required"

    return {
        "needs_adjustment": True,
        "status": status_str,
        "message": f"Recommended adjustments bring predicted strength from {predicted_strength:.2f} MPa to {final_strength:.2f} MPa (Target: {min_strength} MPa).",
        "recommendations": rec_steps,
        "original_mix": ingredients.copy(),
        "adjusted_mix": adj_mix,
        "original_strength": predicted_strength,
        "adjusted_strength": final_strength,
        "initial_compliance": initial_compliance,
        "adjusted_compliance": final_compliance
    }
