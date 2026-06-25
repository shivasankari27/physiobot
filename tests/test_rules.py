from config import EXERCISES
from feedback.rules import danger_detected, feedback_text, quality_score

ARM_RAISE = EXERCISES["arm_raise"]
BICEP_CURL = EXERCISES["bicep_curl"]


def test_quality_score_perfect_form():
    features = {"arm_angle": 90, "elbow_angle": 170}
    assert quality_score(features, ARM_RAISE) == 100


def test_quality_score_penalizes_low_arm_angle():
    features = {"arm_angle": 50, "elbow_angle": 170}
    score = quality_score(features, ARM_RAISE)
    expected = 100 - (70 - 50) * 0.7
    assert score == int(expected)


def test_quality_score_never_negative():
    features = {"arm_angle": 0, "elbow_angle": 0}
    assert quality_score(features, ARM_RAISE) == 0


def test_bicep_curl_penalizes_insufficient_flexion():
    extended = {"arm_angle": 50, "elbow_angle": 120}
    curled = {"arm_angle": 50, "elbow_angle": 50}
    assert quality_score(curled, BICEP_CURL) > quality_score(extended, BICEP_CURL)


def test_feedback_text_tiers():
    assert "Good" in feedback_text(90)
    assert "Adjust" in feedback_text(70)
    assert "Poor" in feedback_text(50)


def test_danger_detected_arm_raise():
    safe = {"arm_angle": 50, "elbow_angle": 130}
    assert danger_detected(safe, ARM_RAISE) is None

    unsafe_arm = {"arm_angle": 30, "elbow_angle": 170}
    assert danger_detected(unsafe_arm, ARM_RAISE) is not None

    unsafe_elbow = {"arm_angle": 80, "elbow_angle": 100}
    assert "elbow" in danger_detected(unsafe_elbow, ARM_RAISE).lower()


def test_danger_detected_bicep_curl():
    unsafe = {"arm_angle": 50, "elbow_angle": 20}
    message = danger_detected(unsafe, BICEP_CURL)
    assert message is not None
    assert "flexion" in message.lower()
