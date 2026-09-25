import json
from pathlib import Path
from typing import Dict, List, Any

from .paths import get_log_path

class NoveltyEngine:
    def __init__(self, log_path: str = None):
        if log_path is None:
            self.log_path = get_log_path("creation_log.jsonl")
        else:
            self.log_path = Path(log_path)
        self.history = self._load_history()

    def _load_history(self) -> List[Dict[str, Any]]:
        if not self.log_path.exists():
            return []

        history = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        history.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return history

    def calculate_similarity(self, new_design: Dict[str, str], past_design: Dict[str, str]) -> float:
        """
        Calculates similarity between two design attribute dictionaries.
        Weights core concepts more heavily than decorations.
        """
        weights = {
            "occasion": 1.0,
            "theme": 1.0,
            "subject": 2.0,
            "art_style": 1.5,
            "mood": 1.0,
            "palette": 0.5,
            "composition": 0.5
        }

        total_weight = 0.0
        match_score = 0.0

        for key, weight in weights.items():
            val1 = new_design.get(key)
            val2 = past_design.get(key)

            if val1 or val2:
                total_weight += weight
                if val1 == val2 and val1 is not None:
                    match_score += weight

        return match_score / total_weight if total_weight > 0 else 0.0

    def evaluate_novelty(self, design_attributes: Dict[str, str]) -> float:
        """
        Returns a novelty score (1.0 = completely novel, 0.0 = exact duplicate exists).
        """
        if not self.history:
            return 1.0

        max_similarity = 0.0
        for past_entry in self.history:
            sim = self.calculate_similarity(design_attributes, past_entry)
            if sim > max_similarity:
                max_similarity = sim

        return 1.0 - max_similarity

    def add_to_history(self, log_entry: Dict[str, Any]):
        self.history.append(log_entry)
