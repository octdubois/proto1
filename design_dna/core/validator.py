from typing import Dict, Any, List
from .models import DesignDNA
from .ground_truth import GroundTruth
from .compatibility import CompatibilityEngine

class Validator:
    def __init__(self, ground_truth: GroundTruth, compatibility: CompatibilityEngine):
        self.ground_truth = ground_truth
        self.compatibility = compatibility

    def validate_dna(self, dna: DesignDNA) -> List[str]:
        """
        Validates the generated DNA against the Ground Truth and Rules.
        Returns a list of error strings. Empty list means valid.
        """
        errors = []

        # Extract selected IDs
        ids_to_check = {
            "occasions": dna.context.occasion,
            "themes": dna.context.theme,
            "subjects": dna.design.subject,
            "actions": dna.design.action,
            "art_styles": dna.design.art_style,
            "compositions": dna.design.composition,
            "palettes": dna.design.palette
        }

        # Check existence
        for category, entity_id in ids_to_check.items():
            if entity_id and not self.ground_truth.validate_reference(category, entity_id):
                errors.append(f"Invalid reference: '{entity_id}' in category '{category}'")

        # Check moods and decorations (lists)
        for mood_id in dna.design.mood:
            if not self.ground_truth.validate_reference("moods", mood_id):
                errors.append(f"Invalid reference: '{mood_id}' in category 'moods'")

        for dec_id in dna.design.decorations:
            if not self.ground_truth.validate_reference("decorations", dec_id):
                errors.append(f"Invalid reference: '{dec_id}' in category 'decorations'")

        # Check hard incompatibilities
        selected_ids = [v for v in ids_to_check.values() if v] + dna.design.mood + dna.design.decorations
        compat_score = self.compatibility.calculate_design_compatibility(selected_ids)

        if compat_score == 0.0:
            errors.append("Design contains hard incompatibilities.")

        return errors
