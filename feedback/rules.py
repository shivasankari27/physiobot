from config import ExerciseConfig


def quality_score(features: dict, exercise: ExerciseConfig) -> int:
    """
    Compute movement quality (0–100) from biomechanical features.
    Safety is prioritized over performance.
    """
    score = 100.0
    arm_angle = features["arm_angle"]
    elbow_angle = features["elbow_angle"]

    if arm_angle < exercise.arm_angle_threshold:
        score -= (exercise.arm_angle_threshold - arm_angle) * exercise.arm_angle_weight

    if exercise.elbow_scoring == "extension":
        if elbow_angle < exercise.elbow_angle_threshold:
            score -= (
                exercise.elbow_angle_threshold - elbow_angle
            ) * exercise.elbow_angle_weight
    else:
        if elbow_angle > exercise.elbow_angle_threshold:
            score -= (
                elbow_angle - exercise.elbow_angle_threshold
            ) * exercise.elbow_angle_weight

    return max(0, int(score))


def feedback_text(score: int) -> str:
    if score > 85:
        return "Good form - maintain posture"
    if score > 65:
        return "Adjust alignment slightly"
    return "Poor form - correct posture"


def danger_detected(features: dict, exercise: ExerciseConfig) -> str | None:
    arm_angle = features["arm_angle"]
    elbow_angle = features["elbow_angle"]

    if arm_angle < exercise.danger_arm_angle:
        return "High injury risk: stop and reset posture"

    if exercise.elbow_scoring == "extension":
        if elbow_angle < exercise.danger_elbow_angle:
            return "Unsafe elbow position detected"
    else:
        if elbow_angle < exercise.danger_elbow_angle:
            return "Unsafe elbow flexion — reduce curl depth"

    return None
