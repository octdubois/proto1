import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "design_dna" / "data" / "ground_truth.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

for occ in data.get("occasions", []):
    name = occ.get("name")
    if name == "Easter":
        occ["family"] = "Holiday"
        occ["tags"].extend(["spring", "cute", "rabbit", "floral", "holiday"])
        occ["preferred_moods"].extend(["Happy", "Playful", "Cute"])
        occ["preferred_styles"].extend(["Illustration", "Kawaii"])
        occ["preferred_palettes"].extend(["Pastel", "Spring"])
    elif name == "Thanksgiving":
        occ["family"] = "Holiday"
        occ["tags"].extend(["autumn", "harvest", "holiday", "family"])
        occ["preferred_moods"].extend(["Cozy", "Warm"])
        occ["preferred_palettes"].extend(["Earth Tones", "Autumn"])
    elif name == "St. Patrick's Day":
        occ["family"] = "Holiday"
        occ["tags"].extend(["spring", "luck", "holiday", "green"])
        occ["preferred_moods"].extend(["Playful", "Energetic"])
        occ["preferred_palettes"].extend(["Green", "Gold"])
    elif name == "Spring":
        occ["tags"].extend(["floral", "nature", "warm", "pastel"])
        occ["preferred_moods"].extend(["Peaceful", "Happy"])
    elif name == "Winter":
        occ["tags"].extend(["cold", "snow", "ice", "dark"])
        occ["preferred_moods"].extend(["Cozy", "Mysterious"])
        occ["preferred_palettes"].extend(["Cool Tones", "Monochrome"])

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Patched Easter and related metadata successfully.")
