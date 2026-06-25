import cv2  
  
  
def draw_status(frame, score, feedback, trend="stable"):  
    cv2.putText(  
        frame,  
        f"Score: {score}",  
        (30, 40),  
        cv2.FONT_HERSHEY_SIMPLEX,  
        1,  
        (0, 255, 0),  
        2  
    )  
  
    cv2.putText(  
        frame,  
        feedback,  
        (30, 80),  
        cv2.FONT_HERSHEY_SIMPLEX,  
        0.8,  
        (255, 255, 0),  
        2  
    )  
  
    cv2.putText(  
        frame,  
        f"Trend: {trend}",  
        (30, 120),  
        cv2.FONT_HERSHEY_SIMPLEX,  
        0.8,  
        (255, 255, 255),  
        2  
    )
