import json
from pathlib import Path
from typing import List, Dict

class CompatibilityRule:
    def __init__(self, source: str, target: str, score: float):
        self.source = source
        self.target = target
        self.score = score

from .paths import get_data_path

class CompatibilityEngine:
    def __init__(self, file_path: str = None):
        if file_path is None:
            self.file_path = get_data_path("compatibility_rules.json")
        else:
            self.file_path = Path(file_path)
        self.rules: List[CompatibilityRule] = self._load()

    def _load(self) -> List[CompatibilityRule]:
        if not self.file_path.exists():
            return []

        with open(self.file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        return [CompatibilityRule(**rule) for rule in raw_data]

    def get_score(self, source_id: str, target_id: str) -> float:
        """
        Gets the compatibility score between two entities.
        If no explicit rule exists, returns 0.5 (neutral).
        """
        for rule in self.rules:
            if (rule.source == source_id and rule.target == target_id) or \
               (rule.source == target_id and rule.target == source_id):
                return rule.score
        return 0.5

    def calculate_aggregate_score(self, target_id: str, context_ids: List[str]) -> float:
        """
        Calculates how compatible a target is with a list of already-selected context items.
        Returns the average score, but treats 0.0 as a hard incompatibility.
        """
        if not context_ids:
            return 0.5

        scores = [self.get_score(ctx, target_id) for ctx in context_ids if ctx]
        if not scores:
            return 0.5

        # Hard incompatibility
        if any(s == 0.0 for s in scores):
            return 0.0

        return sum(scores) / len(scores)

    def calculate_design_compatibility(self, selected_ids: List[str]) -> float:
        """
        Calculates the overall compatibility of a completed design.
        """
        valid_ids = [i for i in selected_ids if i]
        if len(valid_ids) < 2:
            return 1.0

        total_score = 0.0
        pairs = 0
        for i in range(len(valid_ids)):
            for j in range(i + 1, len(valid_ids)):
                score = self.get_score(valid_ids[i], valid_ids[j])
                if score == 0.0:
                    return 0.0
                total_score += score
                pairs += 1

        return total_score / pairs if pairs > 0 else 1.0
