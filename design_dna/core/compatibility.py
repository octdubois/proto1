import json
from pathlib import Path
from typing import List, Dict

from typing import Optional

class CompatibilityRule:
    def __init__(self, source: str, target: str, score: float, relationship_type: str = "symmetric"):
        self.source = source
        self.target = target
        self.score = score
        self.relationship_type = relationship_type

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

    def get_score_with_reason(self, source_id: str, target_id: str, ground_truth=None) -> (float, str):
        """
        Gets the authoritative compatibility score between two entities and returns the reason.
        """
        # 1. Check strict directional rule (Source -> Target)
        for rule in self.rules:
            if rule.source == source_id and rule.target == target_id and rule.relationship_type == "directional":
                return rule.score, f"Explicit directional rule: {source_id} -> {target_id} = {rule.score}"

        # 2. Check symmetric rule
        for rule in self.rules:
            if rule.relationship_type != "directional":
                if (rule.source == source_id and rule.target == target_id) or \
                   (rule.source == target_id and rule.target == source_id):
                    return rule.score, f"Explicit symmetric rule: {source_id} <-> {target_id} = {rule.score}"

        # 3. Dynamic Intrinsic Affinity Calculation
        if ground_truth:
            source_entity = ground_truth.get_entity_by_id(source_id)
            target_entity = ground_truth.get_entity_by_id(target_id)

            if source_entity and target_entity:
                score = 0.5
                reasons = []

                # Check for shared tags
                shared_tags = set(source_entity.tags).intersection(set(target_entity.tags))
                if shared_tags:
                    score += 0.15 * len(shared_tags)
                    reasons.append(f"Shared tags {list(shared_tags)}")

                # Check cross-affinities
                def check_affinity(preferred_list, target_attrs):
                    for pref in preferred_list:
                        for attr in target_attrs:
                            if attr and pref.lower() in attr.lower():
                                return True, pref
                    return False, None

                target_identifiers = [target_entity.name, target_entity.family, target_entity.subcategory]
                source_identifiers = [source_entity.name, source_entity.family, source_entity.subcategory]

                source_prefs = (
                    getattr(source_entity, "preferred_themes", []) +
                    getattr(source_entity, "preferred_subjects", []) +
                    getattr(source_entity, "preferred_decorations", []) +
                    getattr(source_entity, "preferred_moods", []) +
                    getattr(source_entity, "preferred_styles", []) +
                    getattr(source_entity, "preferred_palettes", []) +
                    getattr(source_entity, "preferred_compositions", [])
                )

                target_prefs = (
                    getattr(target_entity, "preferred_themes", []) +
                    getattr(target_entity, "preferred_subjects", []) +
                    getattr(target_entity, "preferred_decorations", []) +
                    getattr(target_entity, "preferred_moods", []) +
                    getattr(target_entity, "preferred_styles", []) +
                    getattr(target_entity, "preferred_palettes", []) +
                    getattr(target_entity, "preferred_compositions", [])
                )

                # Source prefers Target
                s_pref, s_val = check_affinity(source_prefs, target_identifiers)
                if s_pref:
                    score += 0.25
                    reasons.append(f"Source explicit affinity for '{s_val}'")

                # Target prefers Source
                t_pref, t_val = check_affinity(target_prefs, source_identifiers)
                if t_pref:
                    score += 0.25
                    reasons.append(f"Target explicit affinity for '{t_val}'")

                final_score = min(1.0, score)
                if reasons:
                    return final_score, f"Intrinsic Affinity ({final_score:.2f}): " + ", ".join(reasons)
                return 0.05, "Neutral fallback (no semantic overlap)"

        return 0.05, "Neutral fallback (no explicit rule or ground truth data)"

    def get_score(self, source_id: str, target_id: str, ground_truth=None) -> float:
        score, _ = self.get_score_with_reason(source_id, target_id, ground_truth)
        return score

    def calculate_aggregate_score_with_trace(self, target_id: str, context_ids: List[str], ground_truth=None, anchor_id: str = None) -> (float, List[str]):
        if not context_ids:
            return 0.05, ["No context provided"]

        # Optional Whitelist Filtering based on the primary anchor
        if ground_truth and anchor_id:
            anchor_entity = ground_truth.get_entity_by_id(anchor_id)
            target_entity = ground_truth.get_entity_by_id(target_id)

            if anchor_entity and target_entity:
                # Filter by allowed themes
                if getattr(anchor_entity, "allowed_themes", []) and target_id.startswith("thm_"):
                    if target_entity.name not in anchor_entity.allowed_themes:
                        return 0.0, [f"Blocked by anchor whitelist: '{target_entity.name}' not in allowed themes"]

                # Filter by allowed subjects
                if getattr(anchor_entity, "allowed_subject_families", []) and target_id.startswith("sub_"):
                    if target_entity.family not in anchor_entity.allowed_subject_families:
                        return 0.0, [f"Blocked by anchor whitelist: '{target_entity.family}' not in allowed subject families"]

        results = [self.get_score_with_reason(ctx, target_id, ground_truth) for ctx in context_ids if ctx]
        if not results:
            return 0.05, ["No valid context items found"]

        scores = [r[0] for r in results]
        reasons = [r[1] for r in results]

        # Hard incompatibility
        if any(s == 0.0 for s in scores):
            for i, s in enumerate(scores):
                if s == 0.0:
                    return 0.0, [f"HARD INCOMPATIBILITY: {reasons[i]}"]

        # To prevent the context max() hijack, we evaluate the score against the Anchor (if present).
        # The item must not be severely penalized by the primary anchor.
        if anchor_id and anchor_id in context_ids:
            anchor_idx = context_ids.index(anchor_id)
            anchor_score = scores[anchor_idx]
            # If the item has zero affinity with the anchor, don't let a secondary context item push it to 1.0.
            # We cap the max score based on its relationship with the anchor.
            if anchor_score <= 0.05:
                # Highly penalized by the anchor
                return anchor_score, [f"Severely capped by anchor score: {reasons[anchor_idx]}"]

        # We take the maximum score so that strong affinities propagate through the pipeline.
        max_score = max(scores)

        # Filter reasons to only those contributing to the max score
        max_reasons = [reasons[i] for i, s in enumerate(scores) if s == max_score]
        return max_score, max_reasons

    def calculate_aggregate_score(self, target_id: str, context_ids: List[str], ground_truth=None, anchor_id: str = None) -> float:
        score, _ = self.calculate_aggregate_score_with_trace(target_id, context_ids, ground_truth, anchor_id)
        return score

    def calculate_design_compatibility_with_trace(self, selected_ids: List[str], ground_truth=None) -> (float, Dict[str, str]):
        """
        Calculates the overall compatibility of a completed design and returns a trace dictionary.
        """
        valid_ids = [i for i in selected_ids if i]
        if len(valid_ids) < 2:
            return 1.0, {}

        total_score = 0.0
        pairs = 0
        trace = {}
        for i in range(len(valid_ids)):
            for j in range(i + 1, len(valid_ids)):
                score, reason = self.get_score_with_reason(valid_ids[i], valid_ids[j], ground_truth)
                trace[f"{valid_ids[i]} <-> {valid_ids[j]}"] = reason
                if score == 0.0:
                    return 0.0, trace
                total_score += score
                pairs += 1

        return total_score / pairs if pairs > 0 else 1.0, trace

    def calculate_design_compatibility(self, selected_ids: List[str], ground_truth=None) -> float:
        score, _ = self.calculate_design_compatibility_with_trace(selected_ids, ground_truth)
        return score
