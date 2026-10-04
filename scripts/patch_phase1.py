import json
import uuid
from pathlib import Path

DATA_PATH = Path("design_dna/data/ground_truth.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

def gen_id(prefix): return f"{prefix}_{uuid.uuid4().hex[:6]}"

# 1. Update Occasions
for occ in data.get("occasions", []):
    name = occ.get("name")
    if name == "Christmas":
        occ["tags"] = ["christmas", "holiday", "winter", "festive", "snow", "joy"]
        occ["pillar"] = "Seasonal & Holiday"
        occ["allowed_themes"] = ["Cozy", "Whimsical", "Baking", "Candy Store", "Winter"]
        occ["allowed_subject_families"] = ["Holiday Icons", "Animals", "Nature", "Food"]
        occ["preferred_decorations"] = ["Snowflakes", "Stars", "Borders", "Ornaments"]
    elif name == "Halloween":
        occ["tags"] = ["halloween", "holiday", "autumn", "spooky", "fall", "creepy"]
        occ["pillar"] = "Seasonal & Holiday"
        occ["allowed_themes"] = ["Gothic", "Haunted", "Macabre", "Noir", "Spooky"]
        occ["allowed_subject_families"] = ["Holiday Icons", "Animals", "Fantasy", "Nature"]
        occ["preferred_decorations"] = ["Pumpkins", "Bats", "Spider Webs", "Skulls", "Moon"]
    elif name == "Easter":
        occ["pillar"] = "Seasonal & Holiday"
        occ["allowed_themes"] = ["Kawaii", "Whimsical", "Cozy", "Spring", "Floral"]
        occ["allowed_subject_families"] = ["Holiday Icons", "Animals", "Nature", "Food"]
        occ["preferred_decorations"] = ["Flowers", "Eggs", "Baskets", "Ribbons", "Sun"]
    elif name == "Valentine's Day":
        occ["pillar"] = "Seasonal & Holiday"
        occ["allowed_themes"] = ["Kawaii", "Romantic", "Cozy", "Elegant"]
        occ["allowed_subject_families"] = ["Holiday Icons", "Animals", "Food", "Objects"]
        occ["preferred_decorations"] = ["Hearts", "Flowers", "Ribbons", "Stars", "Arrows"]
    elif name == "Cyber Monday":
        occ["pillar"] = "Event"
        occ["allowed_themes"] = ["Cyberpunk", "Technology", "Futurism", "Synthwave", "Digital"]
        occ["allowed_subject_families"] = ["Technology", "Objects", "Vehicles", "Sci-Fi"]
        occ["preferred_decorations"] = ["Circuits", "Neon Glow", "Geometric Shapes", "Pixels"]
    elif name == "Summer Vacation":
        occ["pillar"] = "Season"
        occ["allowed_themes"] = ["Beach", "Adventure", "Tropical", "Exploration", "Travel"]
        occ["allowed_subject_families"] = ["Nature", "Animals", "Vehicles", "Objects"]
        occ["preferred_decorations"] = ["Sun", "Waves", "Palms", "Shells", "Sunglasses"]

# 2. Add Missing Holiday Anchor Subjects
new_subjects = [
    {"name": "Santa Claus", "family": "Holiday Icons", "subcategory": "Christmas", "tags": ["christmas", "holiday", "winter", "festive", "santa"]},
    {"name": "Snowman", "family": "Holiday Icons", "subcategory": "Christmas", "tags": ["christmas", "holiday", "winter", "snow", "cute"]},
    {"name": "Reindeer", "family": "Holiday Icons", "subcategory": "Christmas", "tags": ["christmas", "holiday", "winter", "animal", "cute"]},
    {"name": "Jack-o'-Lantern", "family": "Holiday Icons", "subcategory": "Halloween", "tags": ["halloween", "holiday", "autumn", "spooky", "pumpkin"]},
    {"name": "Witch", "family": "Holiday Icons", "subcategory": "Halloween", "tags": ["halloween", "holiday", "spooky", "magic", "fantasy"]},
    {"name": "Ghost", "family": "Holiday Icons", "subcategory": "Halloween", "tags": ["halloween", "holiday", "spooky", "creepy", "spirit"]}
]
for s in new_subjects:
    data["subjects"].append({
        "id": gen_id("sub"),
        "name": s["name"],
        "family": s["family"],
        "subcategory": s["subcategory"],
        "complexity": 2,
        "tags": s["tags"],
        "characteristics": ["iconic"],
        "preferred_moods": [], "preferred_styles": [], "preferred_palettes": [], "preferred_compositions": []
    })

# 3. Update Tags on Adjacent Subjects
for sub in data.get("subjects", []):
    name = sub.get("name")
    if name == "Pine Tree":
        sub["tags"] = ["nature", "winter", "christmas", "pine", "tree", "forest"]
    elif name == "Penguin":
        sub["tags"] = ["animal", "winter", "cold", "snow", "ice", "cute"]
    elif name == "Husky":
        sub["tags"] = ["animal", "dogs", "winter", "snow", "cold", "cute"]
    elif name == "Cookie":
        sub["tags"] = ["food", "holiday", "baking", "sweet", "cute"]

# 4. Fix Placeholder Tags
for pal in data.get("palettes", []):
    if pal.get("name") == "Christmas Classic":
        pal["tags"] = ["color", "christmas", "holiday", "winter", "festive"]
    if "pal" in pal.get("tags", []):
        pal["tags"] = ["color", pal.get("name", "").lower(), "theme"]

for dec in data.get("decorations", []):
    if dec.get("name") == "Snowflakes":
        dec["tags"] = ["detail", "winter", "christmas", "snow", "cold"]
    if "dec" in dec.get("tags", []):
        dec["tags"] = ["detail", "geometric", "pattern", "border", dec.get("name", "").lower()]

for typ in data.get("typography", []):
    if "typ" in typ.get("tags", []):
        typ["tags"] = ["font", "vintage", "calligraphy", "pixel", "style", typ.get("name", "").lower()]

for tex in data.get("textures", []):
    if "tex" in tex.get("tags", []):
        tex["tags"] = ["surface", "smooth", "organic", "fabric", "metallic", tex.get("name", "").lower()]

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Phase 1 Ground Truth patching complete.")
