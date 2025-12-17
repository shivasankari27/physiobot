import cv2

from pose.estimator import PoseEstimator
from pose.features import extract_features
from feedback.rules import quality_score, feedback_text, adaptive_feedback
from feedback.session import SessionTracker
from ui.overlay import draw_warning


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: Camera not accessible")
    exit(1)

print("Camera opened successfully")

pose = PoseEstimator()
session = SessionTracker()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = pose.process(frame)
    pose.draw(frame, result)

    if result.pose_landmarks:
        landmarks = result.pose_landmarks.landmark

        
        features = extract_features(landmarks)

      
        raw_score = quality_score(features)
        smoothed_score = session.update(raw_score)
        trend = session.trend()

        feedback = adaptive_feedback(
            feedback_text(raw_score),
            trend
        )

        cv2.putText(frame, f"Score: {int(smoothed_score)}", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, feedback, (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.putText(frame, f"Trend: {trend}", (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

       
        h, w, _ = frame.shape

       
        if features["arm_angle"] < 75:
            ls = landmarks[11]
            draw_warning(frame, ls.x * w, ls.y * h, "Raise arm")

       
        if features["elbow_angle"] < 150:
            le = landmarks[13]
            draw_warning(frame, le.x * w, le.y * h, "Straighten")

    cv2.imshow("PhysioBot - Movement Intelligence", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
