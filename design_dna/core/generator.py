import time
import datetime
import uuid
from typing import Dict, Any, List, Optional
from .models import DesignDNA, GenerationContext, DesignContext, DesignContent, ValidationScores
from .ground_truth import GroundTruth
from .compatibility import CompatibilityEngine
from .randomizer import TemperatureRandomizer
from .novelty import NoveltyEngine
from .validator import Validator

class DesignGenerator:
    def __init__(self,
                 ground_truth: GroundTruth,
                 compatibility: CompatibilityEngine,
                 novelty: NoveltyEngine,
                 validator: Validator):
        self.gt = ground_truth
        self.compat = compatibility
        self.novelty = novelty
        self.validator = validator

    def generate(self, seed: int, temperature: int, locked_fields: Dict[str, str]) -> DesignDNA:
        randomizer = TemperatureRandomizer(seed)
        selected_ids: List[str] = []

        def pick(category: str, key_name: str) -> Optional[str]:
            if key_name in locked_fields and locked_fields[key_name]:
                val = locked_fields[key_name]
                selected_ids.append(val)
                return val

            entities = self.gt.get_entities(category)
            if not entities:
                return None

            def weight_func(entity):
                return self.compat.calculate_aggregate_score(entity.id, selected_ids)

            chosen = randomizer.select_weighted(entities, weight_func, temperature)
            if chosen:
                selected_ids.append(chosen.id)
                return chosen.id
            return None

        # 1. Pipeline Selection
        occasion = pick("occasions", "occasion")
        theme = pick("themes", "theme")
        subject = pick("subjects", "subject")
        action = pick("actions", "action")

        # Moods (pick up to 2)
        moods = []
        if "mood" in locked_fields and locked_fields["mood"]:
            moods = [locked_fields["mood"]]
            selected_ids.extend(moods)
        else:
            m1 = pick("moods", "mood_1")
            if m1: moods.append(m1)
            # Second mood slightly different logic, keep it simple for now

        art_style = pick("art_styles", "art_style")
        composition = pick("compositions", "composition")
        palette = pick("palettes", "palette")

        # Decorations
        decorations = []
        if "decorations" in locked_fields and locked_fields["decorations"]:
             decorations = [locked_fields["decorations"]]
             selected_ids.extend(decorations)
        else:
             d1 = pick("decorations", "decoration_1")
             if d1: decorations.append(d1)

        # 2. Build DNA
        dna = DesignDNA(
            generation=GenerationContext(
                id=f"DNA-{uuid.uuid4().hex[:6].upper()}",
                timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
                seed=seed,
                temperature=temperature
            ),
            context=DesignContext(
                occasion=occasion,
                theme=theme
            ),
            design=DesignContent(
                subject=subject,
                action=action,
                mood=moods,
                art_style=art_style,
                composition=composition,
                palette=palette,
                decorations=decorations
            )
        )

        # 3. Calculate Scores
        compat_score = self.compat.calculate_design_compatibility(selected_ids)

        design_attrs = {
            "occasion": occasion,
            "theme": theme,
            "subject": subject,
            "art_style": art_style,
            "mood": moods[0] if moods else None,
            "palette": palette,
            "composition": composition
        }
        novelty_score = self.novelty.evaluate_novelty(design_attrs)

        dna.validation = ValidationScores(
            compatibility_score=round(compat_score, 2),
            novelty_score=round(novelty_score, 2)
        )

        return dna
