PhysioBot — Safety-Aware Rehab Intelligence
A computer vision-based rehabilitation system that provides real-time movement quality assessment and safety feedback for physical therapy exercises.

Features
Real-time Pose Estimation: Uses MediaPipe to track skeletal landmarks and calculate biomechanical angles
Quality Scoring: Evaluates movement form on a 0-100 scale based on arm and elbow angles
Safety Override: Detects dangerous positions and displays immediate injury risk warnings
Session Tracking: Monitors performance trends over time with a sliding window of scores
Visual Feedback: Real-time overlay showing score, feedback messages, and performance trends
Installation
Prerequisites
Python 3.7+
Webcam or camera device
Dependencies
pip install opencv-python mediapipe
Usage
Run the application:

python app.py
The application will open a window displaying:

Your skeletal overlay
Real-time quality score (0-100)
Form feedback messages
Performance trend indicator
Safety warnings when applicable
Controls
q: Quit the application
Project Structure
physiobot/  
├── app.py                 # Main application entry point  
├── config.py              # Biomechanical thresholds and weights  
├── pose/  
│   ├── estimator.py       # MediaPipe pose estimation wrapper  
│   └── features.py        # Biomechanical angle calculations  
├── feedback/  
│   ├── rules.py           # Quality scoring and danger detection  
│   └── session.py         # Session tracking and trend analysis  
└── ui/  
    └── overlay.py         # UI rendering for status display  
Biomechanical Assessment
The system evaluates two key angles:

Arm Angle: Angle at the shoulder formed by hip-shoulder-elbow (ideal: >70°) features.py:31
Elbow Angle: Angle at the elbow formed by shoulder-elbow-wrist (ideal: >160°) features.py:32
Safety Thresholds
Danger Zone (Arm): <40° triggers "High injury risk" warning
Danger Zone (Elbow): <120° triggers "Unsafe elbow position" warning
Configuration
Biomechanical thresholds can be adjusted in config.py:

ARM_ANGLE_THRESHOLD = 70      # Minimum safe arm angle  
ELBOW_ANGLE_THRESHOLD = 160   # Minimum safe elbow angle  
ARM_ANGLE_WEIGHT = 0.7        # Scoring weight for arm deviations  
ELBOW_ANGLE_WEIGHT = 0.5      # Scoring weight for elbow deviations  
DANGER_ARM_ANGLE = 40         # Critical danger threshold for arm  
DANGER_ELBOW_ANGLE = 120      # Critical danger threshold for elbow
