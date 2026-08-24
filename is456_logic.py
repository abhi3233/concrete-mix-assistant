"""
IS 456:2000 Logic Layer
Contains reference specifications for concrete grades (Table 5), grade classification logic,
and independent IS 456 compliance checking (Min Cement Content & Max Water-Cement Ratio).
"""

IS456_SPECS = {
    "M20": {
        "min_strength": 20.0,
        "min_cement": 300.0,
        "max_wc": 0.55
    },
    "M25": {
        "min_strength": 25.0,
        "min_cement": 300.0,
        "max_wc": 0.50
    },
    "M30": {
        "min_strength": 30.0,
        "min_cement": 320.0,
        "max_wc": 0.45
    },
    "M35": {
        "min_strength": 35.0,
        "min_cement": 340.0,
        "max_wc": 0.45
    },
    "M40": {
        "min_strength": 40.0,
        "min_cement": 360.0,
        "max_wc": 0.40
    }
}

AVAILABLE_GRADES = list(IS456_SPECS.keys())

def classify_grade(predicted_strength: float) -> str:
    """
    Maps predicted 28-day compressive strength (in MPa) to standard IS 456 grade.
    """
    if predicted_strength < 20.0:
        return "Below-grade (< M20)"
    elif predicted_strength < 25.0:
        return "M20"
    elif predicted_strength < 30.0:
        return "M25"
    elif predicted_strength < 35.0:
        return "M30"
    elif predicted_strength < 40.0:
        return "M35"
    else:
        return "M40 and above (M40+)"

def calculate_wc_ratio(water: float, cement: float) -> float:
    """
    Calculates Water-Cement Ratio strictly as Water / Cement.
    Per IS 456 Table 5 instructions, fly ash and slag do not count in denominator.
    """
    if cement <= 0:
        return float('inf')
    return water / cement

def check_is456_compliance(cement: float, water: float, target_grade: str) -> dict:
    """
    Independently checks if the mix satisfies IS 456:2000 Table 5 requirements for target_grade.
    Returns detailed compliance status and reasons.
    """
    if target_grade not in IS456_SPECS:
        raise ValueError(f"Invalid target grade: {target_grade}. Allowed: {AVAILABLE_GRADES}")

    spec = IS456_SPECS[target_grade]
    min_cement = spec["min_cement"]
    max_wc = spec["max_wc"]
    min_strength = spec["min_strength"]

    wc_ratio = calculate_wc_ratio(water, cement)

    cement_pass = cement >= min_cement
    wc_pass = wc_ratio <= max_wc

    reasons = []
    if not cement_pass:
        reasons.append(f"Cement content ({cement:.1f} kg/m³) is below minimum requirement of {min_cement:.1f} kg/m³ for {target_grade}.")
    if not wc_pass:
        reasons.append(f"Water-Cement ratio ({wc_ratio:.3f}) exceeds maximum allowed ratio of {max_wc:.2f} for {target_grade}.")

    is_compliant = cement_pass and wc_pass

    return {
        "target_grade": target_grade,
        "is_compliant": is_compliant,
        "cement_pass": cement_pass,
        "cement_actual": cement,
        "min_cement_required": min_cement,
        "wc_pass": wc_pass,
        "wc_actual": wc_ratio,
        "max_wc_allowed": max_wc,
        "min_strength_required": min_strength,
        "reasons": reasons
    }

def check_mix_weight(ingredients: dict, target_weight: float = 2400.0, tolerance: float = 200.0) -> dict:
    """
    Checks if total mix weight per m³ is close to standard concrete density (~2400 kg/m³).
    """
    keys = ["cement", "blast_furnace_slag", "fly_ash", "water", "superplasticizer", "coarse_aggregate", "fine_aggregate"]
    total_weight = sum(float(ingredients.get(k, 0.0)) for k in keys)
    diff = total_weight - target_weight
    is_optimal = abs(diff) <= tolerance

    return {
        "total_weight": total_weight,
        "target_weight": target_weight,
        "diff": diff,
        "is_optimal": is_optimal,
        "message": f"Total Mix Weight: {total_weight:.1f} kg/m³ (Target ≈ {target_weight:.0f} kg/m³)"
    }
