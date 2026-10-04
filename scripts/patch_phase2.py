import json
from pathlib import Path

DATA_PATH = Path("design_dna/data/ground_truth.json")
RULES_PATH = Path("design_dna/data/compatibility_rules.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    gt = json.load(f)

def find_id(category, name):
    for item in gt.get(category, []):
        if item.get("name") == name:
            return item.get("id")
    return None

christmas_id = find_id("occasions", "Christmas")
halloween_id = find_id("occasions", "Halloween")

pal_christmas = find_id("palettes", "Christmas Classic")
dec_snowflakes = find_id("decorations", "Snowflakes")
sub_pine = find_id("subjects", "Pine Tree")
sub_santa = find_id("subjects", "Santa Claus")
sub_snowman = find_id("subjects", "Snowman")
sub_reindeer = find_id("subjects", "Reindeer")
thm_cozy = find_id("themes", "Cozy")

env_cyberpunk = find_id("environments", "Cyberpunk Slums")
env_neon = find_id("environments", "Neon City")
env_volcano = find_id("environments", "Volcano")
env_beach = find_id("environments", "Beach")
env_desert = find_id("environments", "Desert")
thm_cyberpunk = find_id("themes", "Cyberpunk")
pal_pastel = find_id("palettes", "Pastel")

with open(RULES_PATH, "r", encoding="utf-8") as f:
    rules = json.load(f)

# High affinity mappings for Christmas
new_rules = [
    {"source": christmas_id, "target": pal_christmas, "score": 1.0, "relationship_type": "directional"},
    {"source": christmas_id, "target": dec_snowflakes, "score": 0.95, "relationship_type": "directional"},
    {"source": christmas_id, "target": sub_pine, "score": 0.90, "relationship_type": "directional"},
    {"source": christmas_id, "target": sub_santa, "score": 1.0, "relationship_type": "directional"},
    {"source": christmas_id, "target": sub_snowman, "score": 0.95, "relationship_type": "directional"},
    {"source": christmas_id, "target": sub_reindeer, "score": 0.95, "relationship_type": "directional"},
    {"source": christmas_id, "target": thm_cozy, "score": 0.95, "relationship_type": "directional"},
]

# Hard incompatibility rules (0.0)
clashes = [
    (christmas_id, env_cyberpunk),
    (christmas_id, env_neon),
    (christmas_id, env_volcano),
    (christmas_id, env_beach),
    (christmas_id, env_desert),
    (christmas_id, thm_cyberpunk),
    (halloween_id, pal_pastel)
]

for s, t in clashes:
    if s and t:
        new_rules.append({"source": s, "target": t, "score": 0.0, "relationship_type": "symmetric"})

# Deduplicate
existing_pairs = {(r["source"], r["target"]) for r in rules}
for r in new_rules:
    if (r["source"], r["target"]) not in existing_pairs and r["source"] and r["target"]:
        rules.append(r)

with open(RULES_PATH, "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=2)

print("Phase 2 Compatibility Rules patching complete.")
