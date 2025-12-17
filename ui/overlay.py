import cv2

def draw_warning(frame, x, y, text):
    cv2.circle(frame, (int(x), int(y)), 12, (0, 0, 255), -1)
    cv2.putText(
        frame,
        text,
        (int(x) + 10, int(y) - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 255),
        2
    )
