from config import (  
    ARM_ANGLE_THRESHOLD, ELBOW_ANGLE_THRESHOLD,  
    ARM_ANGLE_WEIGHT, ELBOW_ANGLE_WEIGHT,  
    DANGER_ARM_ANGLE, DANGER_ELBOW_ANGLE  
)  
  
  
def quality_score(features):  
    """  
    Computes movement quality score (0–100) based on biomechanical features.  
    Safety is prioritized over performance.  
    """  
    score = 100  
  
    if features["arm_angle"] < ARM_ANGLE_THRESHOLD:  
        score -= (ARM_ANGLE_THRESHOLD - features["arm_angle"]) * ARM_ANGLE_WEIGHT  
  
    if features["elbow_angle"] < ELBOW_ANGLE_THRESHOLD:  
        score -= (ELBOW_ANGLE_THRESHOLD - features["elbow_angle"]) * ELBOW_ANGLE_WEIGHT  
  
    return max(0, int(score))  
  
  
def feedback_text(score):  
    if score > 85:  
        return "Good form — maintain posture"  
    elif score > 65:  
        return "Adjust alignment slightly"  
    else:  
        return "Poor form — correct posture"  
  
  
def danger_detected(features):  
    if features["arm_angle"] < DANGER_ARM_ANGLE:  
        return "High injury risk: stop and reset posture"  
  
    if features["elbow_angle"] < DANGER_ELBOW_ANGLE:  
        return "Unsafe elbow position detected"  
  
    return None
