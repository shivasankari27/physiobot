def quality_score(features):
    score = 100

    if features["arm_angle"] < 70:
        score -= 30
    elif features["arm_angle"] < 85:
        score -= 15

    if features["elbow_angle"] < 150:
        score -= 20

    if features["shoulder_tilt"] > 0.05:
        score -= 15

    return max(score, 0)

def feedback_text(score):
    if score < 50:
        return "Raise your arm higher and keep it straight"
    elif score < 75:
        return "Good, but straighten your arm"
    else:
        return "Excellent form!"

def adaptive_feedback(base_text, trend):
    if trend == "improving":
        return f"{base_text} ↑ Great progress!"
    elif trend == "declining":
        return f"{base_text} ↓ Slow down and focus"
    elif trend == "warming up":
        return "Getting started — follow the guidance"
    return base_text
