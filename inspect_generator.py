import sys
from collections import Counter
from design_dna.core.ground_truth import GroundTruth
from design_dna.core.compatibility import CompatibilityEngine
from design_dna.core.novelty import NoveltyEngine
from design_dna.core.validator import Validator
from design_dna.core.generator import DesignGenerator

gt = GroundTruth()
ce = CompatibilityEngine()
ne = NoveltyEngine()
ve = Validator(gt, ce)
gen = DesignGenerator(gt, ce, ne, ve)

christmas_id = next(o.id for o in gt.get_entities("occasions") if o.name == "Christmas")
locked = {"occasion": christmas_id}

dna = gen.generate(1234, 50, locked)
print(f"Generated Theme: {gt.get_entity_by_id(dna.context.theme).name}")

# Let's verify what happens internally.
