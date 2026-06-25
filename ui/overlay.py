from typing import Any

import cv2

Color = tuple[int, int, int]


def draw_status(
    frame: Any,
    score: int,
    feedback: str,
    trend: str = "stable",
    exercise_name: str | None = None,
    side: str | None = None,
    danger: str | None = None,
) -> None:
    """Render score, feedback, trend, exercise context, and safety warnings."""
    cv2.putText(
        frame,
        f"Score: {score}",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        frame,
        feedback,
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2,
    )

    cv2.putText(
        frame,
        f"Trend: {trend}",
        (30, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    if exercise_name:
        context = exercise_name
        if side:
            context = f"{exercise_name} ({side} arm)"
        cv2.putText(
            frame,
            context,
            (30, frame.shape[0] - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (200, 200, 200),
            2,
        )

    if danger:
        cv2.putText(
            frame,
            danger,
            (30, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            3,
        )
