class SessionTracker:  
    def __init__(self):  
        self.history = []  
  
    def update(self, score):  
        self.history.append(score)  
        if len(self.history) > 30:  
            self.history.pop(0)  
  
    def trend(self):  
        if len(self.history) < 2:  
            return "stable"  
  
        if self.history[-1] > self.history[0]:  
            return "improving"  
        elif self.history[-1] < self.history[0]:  
            return "declining"  
        return "stable"
