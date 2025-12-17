import math


def calculate_angle(a, b, c):
    """
    Returns angle (in degrees) at point b given three landmarks.
    """
    ba = (a.x - b.x, a.y - b.y)
    bc = (c.x - b.x, c.y - b.y)

    dot = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
    mag_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

    if mag_ba * mag_bc == 0:
        return 0

    angle = math.degrees(math.acos(dot / (mag_ba * mag_bc)))
    return angle


def extract_features(landmarks):
    """
    Extracts biomechanical features required for evaluation.
    """
    shoulder = landmarks[11]
    elbow = landmarks[13]
    wrist = landmarks[15]
    hip = landmarks[23]

    arm_angle = calculate_angle(hip, shoulder, elbow)
    elbow_angle = calculate_angle(shoulder, elbow, wrist)

    return {
        "arm_angle": arm_angle,
        "elbow_angle": elbow_angle
    }
