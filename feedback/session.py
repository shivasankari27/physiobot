class SessionTracker:
    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.smoothed_score = None
        self.history = []

    def update(self, score):
        if self.smoothed_score is None:
            self.smoothed_score = score
        else:
            self.smoothed_score = (
                self.alpha * score + (1 - self.alpha) * self.smoothed_score
            )
        self.history.append(self.smoothed_score)
        return self.smoothed_score

    def trend(self):
        if len(self.history) < 5:
            return "warming up"
        delta = self.history[-1] - self.history[-5]
        if delta > 5:
            return "improving"
        elif delta < -5:
            return "declining"
        return "stable"
