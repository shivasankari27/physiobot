from config import EXERCISES
from pose.features import calculate_angle, detect_active_side, extract_features


class MockLandmark:
    def __init__(self, x: float, y: float, visibility: float = 1.0):
        self.x = x
        self.y = y
        self.visibility = visibility


def make_landmarks(indices: dict[int, MockLandmark] | None = None) -> list[MockLandmark]:
    landmarks = [MockLandmark(0, 0, 0) for _ in range(33)]
    if indices:
        for idx, landmark in indices.items():
            landmarks[idx] = landmark
    return landmarks


def test_calculate_angle_right_angle():
    a = MockLandmark(0, 1)
    b = MockLandmark(0, 0)
    c = MockLandmark(1, 0)
    assert abs(calculate_angle(a, b, c) - 90.0) < 0.01


def test_calculate_angle_zero_magnitude_returns_zero():
    a = MockLandmark(0, 0)
    b = MockLandmark(0, 0)
    c = MockLandmark(1, 0)
    assert calculate_angle(a, b, c) == 0.0


def test_calculate_angle_clamps_cosine():
    """Extreme alignment should not raise from floating-point drift."""
    a = MockLandmark(-1, 0)
    b = MockLandmark(0, 0)
    c = MockLandmark(1, 0)
    assert abs(calculate_angle(a, b, c) - 180.0) < 0.01


def test_detect_active_side_prefers_higher_visibility():
    landmarks = make_landmarks(
        {
            11: MockLandmark(0, 0, 0.2),
            13: MockLandmark(0, 0, 0.2),
            15: MockLandmark(0, 0, 0.2),
            12: MockLandmark(0, 0, 0.9),
            14: MockLandmark(0, 0, 0.9),
            16: MockLandmark(0, 0, 0.9),
        }
    )
    assert detect_active_side(landmarks, "auto") == "right"


def test_detect_active_side_honors_fixed_preference():
    landmarks = make_landmarks()
    assert detect_active_side(landmarks, "left") == "left"
    assert detect_active_side(landmarks, "right") == "right"


def test_extract_features_returns_angles_and_side():
    landmarks = make_landmarks(
        {
            23: MockLandmark(0.5, 0.8),  # left hip
            11: MockLandmark(0.5, 0.5),  # left shoulder
            13: MockLandmark(0.2, 0.5),  # left elbow
            15: MockLandmark(0.0, 0.5),  # left wrist
        }
    )
    features = extract_features(landmarks, side="left")
    assert features["side"] == "left"
    assert features["arm_angle"] > 0
    assert features["elbow_angle"] > 80
