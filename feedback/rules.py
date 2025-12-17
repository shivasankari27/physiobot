def quality_score(features):
    """
    Computes movement quality score (0–100) based on biomechanical features.
    Safety is prioritized over performance.
    """
    score = 100

   
    if features["arm_angle"] < 70:
        score -= (70 - features["arm_angle"]) * 0.7

    if features["elbow_angle"] < 160:
        score -= (160 - features["elbow_angle"]) * 0.5

    return max(0, int(score))


def feedback_text(score):
    if score > 85:
        return "Good form — maintain posture"
    elif score > 65:
        return "Adjust alignment slightly"
    else:
        return "Poor form — correct posture"


def danger_detected(features):
    
    if features["arm_angle"] < 40:
        return "High injury risk: stop and reset posture"

    if features["elbow_angle"] < 120:
        return "Unsafe elbow position detected"

    return None
