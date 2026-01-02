import json
import os

class ScoreManager:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                # Migration: Convert old list of ints to dicts
                if data and isinstance(data[0], int):
                    return [{'name': 'Anonymous', 'score': s} for s in data]
                return data
        except (json.JSONDecodeError, IOError):
            return []

    def save_scores(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f)
        except IOError:
            print("Error saving scores")

    def add_score(self, name, score):
        self.scores.append({'name': name, 'score': score})
        # Sort by score descending
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:5] # Keep top 5
        self.save_scores()

    def get_high_scores(self):
        return self.scores
