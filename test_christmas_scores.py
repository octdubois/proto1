import sys
from design_dna.core.ground_truth import GroundTruth
from design_dna.core.compatibility import CompatibilityEngine
import json

gt = GroundTruth()
ce = CompatibilityEngine()

occ_id = next(o.id for o in gt.get_entities("occasions") if o.name == "Christmas")

# Let's see the score for "Double Bass"
sub_db = next(o.id for o in gt.get_entities("subjects") if o.name == "Double Bass")

score, reason = ce.get_score_with_reason(occ_id, sub_db, gt)
print(f"Christmas <-> Double Bass: {score} ({reason})")

thm_gladiator = next(o.id for o in gt.get_entities("themes") if o.name == "Gladiator")
score, reason = ce.get_score_with_reason(occ_id, thm_gladiator, gt)
print(f"Christmas <-> Gladiator Theme: {score} ({reason})")

# Did whitelist filtering fail?
# When generating, calculate_aggregate_score is used:
agg_score = ce.calculate_aggregate_score(thm_gladiator, [occ_id], gt, anchor_id=occ_id)
print(f"Aggregate Score for Gladiator Theme (with Christmas as Anchor): {agg_score}")
