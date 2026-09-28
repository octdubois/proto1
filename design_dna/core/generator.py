import time
import datetime
import uuid
from typing import Dict, Any, List, Optional
from .models import DesignDNA, GenerationContext, DesignContext, DesignContent, ValidationScores, ConceptLayer
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
        primary_subject = pick("subjects", "primary_subject")

        # Calculate secondary subjects based on config and temperature
        # Low temp -> 0 to 1
        # High temp -> up to max_secondary_subjects
        from .config import AppConfig
        config = AppConfig()
        limits = config.generation_limits
        min_sec = limits["min_secondary_subjects"]
        max_sec = limits["max_secondary_subjects"]

        if temperature < 30:
            target_sec_count = randomizer.rng.randint(min_sec, max(min_sec, 1))
        elif temperature > 70:
            target_sec_count = randomizer.rng.randint(min(1, max_sec), max_sec)
        else:
            target_sec_count = randomizer.rng.randint(min_sec, max_sec)

        secondary_subjects = []
        for i in range(target_sec_count):
            sec_sub = pick("subjects", f"secondary_subject_{i+1}")
            if sec_sub and sec_sub != primary_subject and sec_sub not in secondary_subjects:
                secondary_subjects.append(sec_sub)

        action = pick("actions", "action")
        environment = pick("environments", "environment")

        # Concept Formulation
        concept = ConceptLayer(
            relationship="subject_in_environment" if environment else "subject_isolated",
            visual_hook="unexpected_scale" if temperature > 80 else "balanced_presentation",
            narrative_type="character_scene" if action else "portrait"
        )

        # Moods
        moods = []
        if "mood" in locked_fields and locked_fields["mood"]:
            moods = [locked_fields["mood"]]
            selected_ids.extend(moods)
        else:
            m1 = pick("moods", "mood_1")
            if m1: moods.append(m1)

        art_style = pick("art_styles", "art_style")
        visual_style = pick("visual_styles", "visual_style")
        composition = pick("compositions", "composition")
        palette = pick("palettes", "palette")

        # Decorators, Textures, Effects
        decorations = []
        if "decorations" in locked_fields and locked_fields["decorations"]:
             decorations = [locked_fields["decorations"]]
             selected_ids.extend(decorations)
        else:
             d1 = pick("decorations", "decoration_1")
             if d1: decorations.append(d1)

        textures = []
        t1 = pick("textures", "texture_1")
        if t1: textures.append(t1)

        visual_effects = []
        v1 = pick("visual_effects", "effect_1")
        if v1: visual_effects.append(v1)

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
                primary_subject=primary_subject,
                secondary_subjects=secondary_subjects,
                concept=concept,
                action=action,
                environment=environment,
                mood=moods,
                art_style=art_style,
                visual_style=[visual_style] if visual_style else [],
                composition=composition,
                palette=palette,
                decorations=decorations,
                textures=textures,
                visual_effects=visual_effects
            )
        )

        # 3. Calculate Scores
        compat_score = self.compat.calculate_design_compatibility(selected_ids)

        design_attrs = {
            "occasion": occasion,
            "theme": theme,
            "primary_subject": primary_subject,
            "art_style": art_style,
            "mood": moods[0] if moods else None,
            "palette": palette,
            "composition": composition
        }
        novelty_score = self.novelty.evaluate_novelty(design_attrs)

        wildcard_threshold = config.generation_limits.get("wildcard_threshold_temperature", 60)
        dna.validation = ValidationScores(
            compatibility_score=round(compat_score, 2),
            novelty_score=round(novelty_score, 2),
            wildcards_used=temperature >= wildcard_threshold
        )

        return dna
