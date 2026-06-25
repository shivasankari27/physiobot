import cv2  
from feedback.session import SessionTracker  
from pose.estimator import PoseEstimator  
from pose.features import extract_features  
from feedback.rules import (  
    quality_score,  
    feedback_text,  
    danger_detected  
)  
from ui.overlay import draw_status  
  
  
def main():  
    cap = cv2.VideoCapture(0)  
    pose = PoseEstimator()  
    tracker = SessionTracker()  
  
    while True:  
        try:  
            ret, frame = cap.read()  
            if not ret:  
                print("Camera frame read failed")  
                continue  
        except Exception as e:  
            print(f"Camera error: {e}")  
            break  
  
        result = pose.process(frame)  
        pose.draw(frame, result)  
  
        if result.pose_landmarks:  
            landmarks = result.pose_landmarks.landmark  
            features = extract_features(landmarks)  
  
            danger = danger_detected(features)  
            score = quality_score(features)  
            feedback = feedback_text(score)  
  
            tracker.update(score)  
            trend = tracker.trend()  
  
            draw_status(frame, score, feedback, trend)  
  

            if danger:  
                cv2.putText(  
                    frame,  
                    danger,  
                    (30, 160),  
                    cv2.FONT_HERSHEY_SIMPLEX,  
                    0.8,  
                    (0, 0, 255),  
                    3  
                )  
  
        cv2.imshow("PhysioBot — Safety-Aware Rehab Intelligence", frame)  
  
        if cv2.waitKey(1) & 0xFF == ord("q"):  
            break  
  
    cap.release()  
    cv2.destroyAllWindows()  
  
  
if __name__ == "__main__":  
    main()
