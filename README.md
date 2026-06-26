# PhysioBot — Safety-Aware Rehab Intelligence

A computer vision rehabilitation assistant that scores movement quality in real time, detects unsafe positions, and tracks session performance over time.

## Features

- **Real-time pose estimation** — MediaPipe skeletal tracking with biomechanical angle analysis
- **Exercise modes** — Arm raise and bicep curl with per-exercise thresholds and scoring
- **Bilateral support** — Track left or right arm, or auto-select the side with better visibility
- **Quality scoring** — 0–100 form score with contextual feedback messages
- **Safety override** — Immediate warnings when angles enter injury-risk zones
- **Session tracking** — Rolling-mean trend analysis over a sliding window of scores
- **Session persistence** — JSON session logs saved on quit to `data/sessions/`
- **CLI configuration** — Camera index, exercise, and arm side via command-line flags
- **Test suite** — Pytest coverage for angle math, scoring rules, and session logic

## Installation

### Prerequisites

- Python 3.9+
- Webcam or camera device

### Dependencies

```bash
pip install -r requirements.txt
```

For development (includes pytest):

```bash
pip install -e ".[dev]"
```

## Usage

Run with defaults (arm raise, camera 0, auto arm detection):

```bash
python app.py
```

### Options

```bash
python app.py --exercise bicep_curl --camera 0 --arm left
```

| Flag | Choices | Default | Description |
|------|---------|---------|-------------|
| `--exercise` | `arm_raise`, `bicep_curl` | `arm_raise` | Rehab exercise mode |
| `--camera` | integer | `0` | Camera device index |
| `--arm` | `left`, `right`, `auto` | `auto` | Arm to track |

### Controls

- `q` — Quit and save session to `data/sessions/`

### On-screen display

- Quality score (0–100) in green / orange / red based on performance
- Form feedback message
- Performance trend (improving / stable / declining)
- Active exercise and tracked arm
- Red safety warning when danger thresholds are breached

## Testing

```bash
pytest
```

## Project structure
