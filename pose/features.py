import numpy as np
import math

LEFT_SHOULDER = 11
LEFT_ELBOW = 13
LEFT_WRIST = 15
RIGHT_SHOULDER = 12
RIGHT_HIP = 24

def angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

def extract_features(landmarks):
    ls = landmarks[LEFT_SHOULDER]
    le = landmarks[LEFT_ELBOW]
    lw = landmarks[LEFT_WRIST]
    rs = landmarks[RIGHT_SHOULDER]

    arm_angle = angle(
        [le.x, le.y],
        [ls.x, ls.y],
        [rs.x, rs.y]
    )

    elbow_angle = angle(
        [ls.x, ls.y],
        [le.x, le.y],
        [lw.x, lw.y]
    )

    shoulder_tilt = abs(ls.y - rs.y)

    return {
        "arm_angle": arm_angle,
        "elbow_angle": elbow_angle,
        "shoulder_tilt": shoulder_tilt
    }
