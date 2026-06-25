from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExerciseConfig:
    """Biomechanical thresholds and scoring weights for a rehab exercise."""

    name: str
    arm_angle_threshold: float
    elbow_angle_threshold: float
    arm_angle_weight: float
    elbow_angle_weight: float
    danger_arm_angle: float
    danger_elbow_angle: float
    elbow_scoring: str = "extension"  # "extension" or "flexion"


EXERCISES: dict[str, ExerciseConfig] = {
    "arm_raise": ExerciseConfig(
        name="Arm Raise",
        arm_angle_threshold=70,
        elbow_angle_threshold=160,
        arm_angle_weight=0.7,
        elbow_angle_weight=0.5,
        danger_arm_angle=40,
        danger_elbow_angle=120,
        elbow_scoring="extension",
    ),
    "bicep_curl": ExerciseConfig(
        name="Bicep Curl",
        arm_angle_threshold=45,
        elbow_angle_threshold=60,
        arm_angle_weight=0.5,
        elbow_angle_weight=0.6,
        danger_arm_angle=30,
        danger_elbow_angle=25,
        elbow_scoring="flexion",
    ),
}

DEFAULT_EXERCISE = "arm_raise"
DEFAULT_CAMERA_INDEX = 0
SESSION_HISTORY_SIZE = 30
TREND_WINDOW = 5
TREND_THRESHOLD = 3.0

DATA_DIR = Path("data/sessions")
WINDOW_TITLE = "PhysioBot — Safety-Aware Rehab Intelligence"

# MediaPipe pose landmark indices
LANDMARKS = {
    "left": {"shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23},
    "right": {"shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24},
}
