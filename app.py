import argparse
import sys

import cv2

from config import DEFAULT_CAMERA_INDEX, DEFAULT_EXERCISE, EXERCISES, WINDOW_TITLE
from feedback.rules import danger_detected, feedback_text, quality_score
from feedback.session import SessionTracker
from pose.estimator import PoseEstimator
from pose.features import extract_features
from ui.overlay import draw_status


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PhysioBot - real-time rehab movement quality assessment"
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=DEFAULT_CAMERA_INDEX,
        help="Camera device index (default: 0)",
    )
    parser.add_argument(
        "--exercise",
        choices=list(EXERCISES.keys()),
        default=DEFAULT_EXERCISE,
        help="Rehab exercise mode (default: arm_raise)",
    )
    parser.add_argument(
        "--arm",
        choices=["left", "right", "auto"],
        default="auto",
        help="Arm to track; auto picks the side with better visibility (default: auto)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    exercise = EXERCISES[args.exercise]

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"Error: could not open camera {args.camera}")
        return 1

    pose = PoseEstimator()
    tracker = SessionTracker(exercise_key=args.exercise)

    print(f"PhysioBot ready - {exercise.name} | camera {args.camera} | arm {args.arm}")
    print("Press 'q' to quit and save session.")

    try:
        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    print("Camera frame read failed")
                    continue
            except Exception as exc:
                print(f"Camera error: {exc}")
                break

            result = pose.process(frame)
            pose.draw(frame, result)

            if result.pose_landmarks:
                landmarks = result.pose_landmarks.landmark
                features = extract_features(landmarks, side=args.arm)

                danger = danger_detected(features, exercise)
                score = quality_score(features, exercise)
                feedback = feedback_text(score)

                tracker.update(score)
                trend = tracker.trend()

                draw_status(
                    frame,
                    score,
                    feedback,
                    trend,
                    exercise_name=exercise.name,
                    side=str(features["side"]),
                    danger=danger,
                    reps=tracker.reps(),
                )

            cv2.imshow(WINDOW_TITLE, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        pose.close()
        cv2.destroyAllWindows()
        saved = tracker.save()
        if saved:
            print(f"Session saved to {saved}")
            print(f"Total reps: {tracker.reps()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
