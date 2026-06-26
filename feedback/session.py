import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

from config import DATA_DIR, SESSION_HISTORY_SIZE, TREND_THRESHOLD, TREND_WINDOW


class SessionTracker:
    def __init__(self, exercise_key: str, max_history: int = SESSION_HISTORY_SIZE):
        self.exercise_key = exercise_key
        self.max_history = max_history
        self.history: deque[int] = deque(maxlen=max_history)
        self.started_at = datetime.now(timezone.utc)

    def update(self, score: int) -> None:
        self.history.append(score)

    def average_score(self) -> float | None:
        if not self.history:
            return None
        return sum(self.history) / len(self.history)

    def trend(self) -> str:
        window = TREND_WINDOW * 2
        if len(self.history) < window:
            return "stable"

        history_list = list(self.history)
        recent = history_list[-TREND_WINDOW:]
        earlier = history_list[-window:-TREND_WINDOW]

        recent_mean = sum(recent) / len(recent)
        earlier_mean = sum(earlier) / len(earlier)
        diff = recent_mean - earlier_mean

        if diff > TREND_THRESHOLD:
            return "improving"
        if diff < -TREND_THRESHOLD:
            return "declining"
        return "stable"

    def save(self) -> Path | None:
        if not self.history:
            return None

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = self.started_at.strftime("%Y%m%d_%H%M%S")
        path = DATA_DIR / f"session_{self.exercise_key}_{timestamp}.json"

        payload = {
            "exercise": self.exercise_key,
            "started_at": self.started_at.isoformat(),
            "ended_at": datetime.now(timezone.utc).isoformat(),
            "scores": list(self.history),
            "average_score": self.average_score(),
            "trend": self.trend(),
        }

        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path
