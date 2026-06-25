import json
from pathlib import Path

import pytest

from feedback.session import SessionTracker


def test_trend_stable_with_insufficient_history():
    tracker = SessionTracker("arm_raise")
    tracker.update(80)
    assert tracker.trend() == "stable"


def test_trend_improving_with_rolling_mean():
    tracker = SessionTracker("arm_raise", max_history=30)
    for score in [60, 62, 64, 66, 68, 70, 72, 74, 76, 78]:
        tracker.update(score)
    assert tracker.trend() == "improving"


def test_trend_declining_with_rolling_mean():
    tracker = SessionTracker("arm_raise", max_history=30)
    for score in [90, 88, 86, 84, 82, 80, 78, 76, 74, 72]:
        tracker.update(score)
    assert tracker.trend() == "declining"


def test_average_score():
    tracker = SessionTracker("arm_raise")
    tracker.update(80)
    tracker.update(90)
    assert tracker.average_score() == 85.0


def test_save_session_writes_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("feedback.session.DATA_DIR", tmp_path)
    tracker = SessionTracker("arm_raise")
    tracker.update(85)
    tracker.update(90)

    path = tracker.save()
    assert path is not None
    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["exercise"] == "arm_raise"
    assert data["scores"] == [85, 90]
    assert data["average_score"] == 87.5


def test_save_returns_none_when_empty():
    tracker = SessionTracker("arm_raise")
    assert tracker.save() is None
