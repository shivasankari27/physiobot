import math
from typing import Any, Literal

from config import LANDMARKS

Side = Literal["left", "right"]


def calculate_angle(a: Any, b: Any, c: Any) -> float:
    """Return the angle in degrees at point b formed by landmarks a-b-c."""
    ba = (a.x - b.x, a.y - b.y)
    bc = (c.x - b.x, c.y - b.y)

    dot = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
    mag_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

    if mag_ba * mag_bc == 0:
        return 0.0

    cosine = max(-1.0, min(1.0, dot / (mag_ba * mag_bc)))
    return math.degrees(math.acos(cosine))


def _landmark_visibility(landmark: Any) -> float:
    return getattr(landmark, "visibility", 1.0)


def detect_active_side(
    landmarks: list[Any],
    preference: Side | Literal["auto"] = "auto",
) -> Side:
    """Pick the arm side with better landmark visibility, or honor a fixed preference."""
    if preference in ("left", "right"):
        return preference

    left_ids = LANDMARKS["left"]
    right_ids = LANDMARKS["right"]

    left_score = sum(
        _landmark_visibility(landmarks[left_ids[key]])
        for key in ("shoulder", "elbow", "wrist")
    )
    right_score = sum(
        _landmark_visibility(landmarks[right_ids[key]])
        for key in ("shoulder", "elbow", "wrist")
    )

    return "left" if left_score >= right_score else "right"


def extract_features(
    landmarks: list[Any],
    side: Side | Literal["auto"] = "auto",
) -> dict[str, float | Side]:
    """Extract biomechanical angles for the selected or auto-detected arm."""
    active_side = detect_active_side(landmarks, side)
    ids = LANDMARKS[active_side]

    shoulder = landmarks[ids["shoulder"]]
    elbow = landmarks[ids["elbow"]]
    wrist = landmarks[ids["wrist"]]
    hip = landmarks[ids["hip"]]

    arm_angle = calculate_angle(hip, shoulder, elbow)
    elbow_angle = calculate_angle(shoulder, elbow, wrist)

    return {
        "arm_angle": arm_angle,
        "elbow_angle": elbow_angle,
        "side": active_side,
    }
