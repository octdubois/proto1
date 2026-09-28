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
        # Bias towards merchandise graphics

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

        # Actions are less critical for merch graphics, keep them optional
        action = pick("actions", "action") if randomizer.rng.random() > 0.3 or ("action" in locked_fields) else None

        # Environments should be rare for merchandise graphics (e.g. t-shirt designs usually float on transparency)
        env_chance = 0.15 + (temperature / 100.0 * 0.2) # 15% to 35% chance
        environment = pick("environments", "environment") if randomizer.rng.random() < env_chance or ("environment" in locked_fields) else None

        # Concept Formulation focused on Merchandise Graphics
        rel_options = ["integrated_graphic_lockup", "subject_with_environmental_framing", "layered_emblem"] if environment else ["spot_illustration", "isolated_motif", "typographic_integration", "floating_graphic"]

        hook_options = ["bold_silhouette", "high_contrast_linework", "balanced_iconography"]
        if temperature > 60:
            hook_options.extend(["distressed_vintage_appeal", "pop_art_juxtaposition", "psychedelic_distortion"])

        narrative_options = ["dynamic_mascot", "action_motif"] if action else ["iconic_emblem", "pattern_element", "statement_graphic", "stylized_insignia"]

        concept = ConceptLayer(
            relationship=randomizer.rng.choice(rel_options),
            visual_hook=randomizer.rng.choice(hook_options),
            narrative_type=randomizer.rng.choice(narrative_options)
        )

        # Moods
        moods = []
        if "mood" in locked_fields and locked_fields["mood"]:
            moods = [locked_fields["mood"]]
            selected_ids.extend(moods)
        else:
            m1 = pick("moods", "mood_1")
            if m1: moods.append(m1)

        # Strongly bias towards graphic/illustration styles for merch
        def style_weight_adj(entity):
            base_score = self.compat.calculate_aggregate_score(entity.id, selected_ids)
            if entity.family in ["Graphic Design", "Illustration", "Digital"]:
                return min(1.0, base_score * 1.5)
            elif entity.family in ["Traditional", "Modern"]:
                return max(0.01, base_score * 0.4)
            return base_score

        if "art_style" in locked_fields and locked_fields["art_style"]:
            art_style = locked_fields["art_style"]
            selected_ids.append(art_style)
        else:
            style_entities = self.gt.get_entities("art_styles")
            chosen_style = randomizer.select_weighted(style_entities, style_weight_adj, temperature) if style_entities else None
            art_style = chosen_style.id if chosen_style else None
            if art_style: selected_ids.append(art_style)

        visual_style = pick("visual_styles", "visual_style")

        # Strongly bias towards standalone compositions
        def comp_weight_adj(entity):
            base_score = self.compat.calculate_aggregate_score(entity.id, selected_ids)
            if entity.name in ["Badge", "Circular Emblem", "Centered", "Logo Lockup", "Sticker", "Patch"]:
                return min(1.0, base_score * 1.8)
            elif "Scene" in entity.name or "Panoramic" in entity.name:
                return max(0.01, base_score * 0.3)
            return base_score

        if "composition" in locked_fields and locked_fields["composition"]:
            composition = locked_fields["composition"]
            selected_ids.append(composition)
        else:
            comp_entities = self.gt.get_entities("compositions")
            chosen_comp = randomizer.select_weighted(comp_entities, comp_weight_adj, temperature) if comp_entities else None
            composition = chosen_comp.id if chosen_comp else None
            if composition: selected_ids.append(composition)

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
