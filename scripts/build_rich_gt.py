import json
import uuid
from pathlib import Path
import random

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "design_dna" / "data" / "ground_truth.json"

def gen_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"

def create_entity(name, prefix, family=None, subcategory=None, tags=None, characteristics=None, p_moods=None, p_styles=None, p_palettes=None):
    return {
        "id": gen_id(prefix),
        "name": name,
        "family": family,
        "subcategory": subcategory,
        "complexity": random.randint(1, 3),
        "tags": tags or [],
        "characteristics": characteristics or [],
        "preferred_moods": p_moods or [],
        "preferred_styles": p_styles or [],
        "preferred_palettes": p_palettes or [],
        "preferred_compositions": []
    }

occasions = [
    create_entity("Halloween", "occ", "Holiday", None, ["spooky", "autumn"], ["festive"], ["Spooky", "Dark"], ["Gothic", "Vintage"], ["Halloween Night"]),
    create_entity("Christmas", "occ", "Holiday", None, ["winter", "joy"], ["festive"], ["Happy", "Cozy"], ["Traditional", "Cartoon"], ["Christmas Classic"]),
    create_entity("Valentine's Day", "occ", "Holiday", None, ["love", "romance"], ["festive"], ["Romantic", "Cute"], ["Kawaii", "Watercolor"], ["Pastel", "Red/Pink"]),
    create_entity("New Year's Eve", "occ", "Holiday", None, ["party", "midnight"], ["festive", "sparkly"], ["Energetic", "Epic"], ["Graphic Design"], ["Neon", "High Contrast"]),
    create_entity("Summer Vacation", "occ", "Season", "Summer", ["beach", "relax"], ["warm", "sunny"], ["Joyful", "Peaceful"], ["Pop Art", "Vintage Poster"], ["Warm Tones", "Vibrant"]),
    create_entity("Cyber Monday", "occ", "Event", "Shopping", ["tech", "sales"], ["digital"], ["Energetic", "Futuristic"], ["Cyberpunk", "Minimal Vector"], ["Neon"]),
]

# Generate more programmatically with metadata
themes_raw = {
    "Dark": [("Gothic", ["dark", "ornate"]), ("Haunted", ["scary", "ghosts"]), ("Macabre", ["death", "skulls"]), ("Noir", ["detective", "shadows"])],
    "Cute": [("Kawaii", ["adorable", "japanese"]), ("Whimsical", ["magical", "soft"]), ("Cozy", ["warm", "relaxing"])],
    "Tech": [("Cyberpunk", ["neon", "future"]), ("Steampunk", ["gears", "victorian"]), ("AI", ["robots", "code"]), ("Space Opera", ["stars", "ships"])]
}
themes = []
for family, items in themes_raw.items():
    for name, tags in items:
        themes.append(create_entity(name, "thm", family, None, tags, [f"Has {tags[0]} vibes"], ["Mysterious" if family=="Dark" else "Happy"], [], []))

# We need ~150 subjects. Let's create specific ones.
subjects = []
animals = {
    "Cats": ["Black Cat", "Persian Cat", "Siamese Cat", "Sphynx Cat", "Bengal Cat", "Maine Coon", "Scottish Fold", "Ragdoll", "British Shorthair", "Abyssinian"],
    "Dogs": ["Golden Retriever", "Pug", "Husky", "Bulldog", "Poodle", "Beagle", "Dachshund", "Corgi", "Shiba Inu", "Dalmatian", "Boxer", "Great Dane"],
    "Birds": ["Owl", "Raven", "Eagle", "Parrot", "Penguin", "Flamingo", "Peacock", "Hummingbird", "Swan", "Toucan"],
    "Wild": ["Wolf", "Fox", "Bear", "Tiger", "Lion", "Elephant", "Giraffe", "Zebra", "Kangaroo", "Panda", "Sloth", "Koala", "Gorilla", "Monkey"]
}
for subcat, names in animals.items():
    for name in names:
        subjects.append(create_entity(name, "sub", "Animals", subcat, ["animal", subcat.lower()], ["furry" if subcat!="Birds" else "feathers"], ["Playful"], ["Illustration", "Cartoon"], []))

fantasy = ["Dragon", "Wizard", "Knight", "Fairy", "Goblin", "Elf", "Orc", "Troll", "Mermaid", "Unicorn", "Pegasus", "Phoenix", "Griffin", "Centaur", "Minotaur"]
for name in fantasy:
    subjects.append(create_entity(name, "sub", "Fantasy", None, ["magic", "myth"], ["magical"], ["Epic", "Mysterious"], ["Concept Art", "Digital Painting"], ["Jewel Tones"]))

tech_objs = ["Robot", "Cyborg", "Mech", "Drone", "AI Core", "Spaceship", "Satellite", "Rover", "Laser Gun", "Hologram"]
for name in tech_objs:
    subjects.append(create_entity(name, "sub", "Technology", None, ["future", "machine"], ["metallic"], ["Futuristic", "Epic"], ["Cyberpunk", "Sci-Fi"], ["Neon"]))

everyday = ["Coffee Cup", "Book", "Camera", "Guitar", "Bicycle", "Typewriter", "Telescope", "Microscope", "Clock", "Compass"]
for name in everyday:
    subjects.append(create_entity(name, "sub", "Objects", None, ["item", "everyday"], ["inanimate"], ["Cozy"], ["Vintage", "Minimal Vector"], ["Earth Tones"]))


actions_raw = ["Sitting", "Standing", "Running", "Flying", "Jumping", "Dancing", "Drinking", "Eating", "Sleeping", "Reading", "Working", "Fighting", "Exploring", "Coding", "Painting", "Meditating", "Casting Magic", "Hovering", "Gliding", "Teleporting", "Transforming"]
actions = [create_entity(a, "act", tags=["movement"]) for a in actions_raw]

envs_raw = {
    "Nature": ["Forest", "Mountain", "Beach", "Desert", "Jungle", "Cave", "Waterfall", "Tundra", "Swamp", "Canyon"],
    "Urban": ["City Street", "Alleyway", "Rooftop", "Coffee Shop", "Library", "Subway Station", "Neon City", "Factory"],
    "Fantasy": ["Haunted Mansion", "Castle", "Magic Academy", "Crystal Cavern", "Floating Island", "Dragon's Lair"],
    "Sci-Fi": ["Space Station", "Alien Planet", "Lunar Base", "Cyberpunk Slums", "Spaceship Bridge", "Wormhole"]
}
environments = []
for fam, items in envs_raw.items():
    for n in items: environments.append(create_entity(n, "env", fam, tags=["location", fam.lower()], p_moods=["Mysterious"] if fam in ["Fantasy", "Sci-Fi"] else ["Peaceful"]))

moods_raw = ["Happy", "Joyful", "Playful", "Cute", "Cozy", "Peaceful", "Mysterious", "Dark", "Eerie", "Spooky", "Epic", "Heroic", "Futuristic", "Surreal", "Melancholy", "Nostalgic", "Energetic", "Aggressive", "Romantic", "Calm"]
moods = [create_entity(m, "mod", tags=["emotion"]) for m in moods_raw]

styles_raw = {
    "Traditional": ["Realism", "Impressionism", "Expressionism", "Surrealism", "Pop Art", "Cubism", "Pointillism", "Renaissance", "Baroque", "Art Nouveau"],
    "Illustration": ["Cartoon", "Comic Book", "Manga", "Anime", "Chibi", "Kawaii", "Line Art", "Watercolor", "Gouache", "Ink Drawing"],
    "Graphic Design": ["Vintage Poster", "Screen Print", "Badge", "Emblem", "Sticker Art", "Flat Vector", "Minimal Vector", "Retro Design"],
    "Digital": ["Digital Painting", "Concept Art", "Low Poly", "Voxel", "Isometric", "Pixel Art", "3D Render", "Clay Render"],
    "Futuristic": ["Cyberpunk", "Steampunk", "Dieselpunk", "Synthwave", "Sci-Fi", "Solarpunk", "Retrofuturism"]
}
art_styles = []
for fam, items in styles_raw.items():
    for n in items: art_styles.append(create_entity(n, "sty", fam, tags=["art", fam.lower()]))

vis_styles = [create_entity(n, "vis", tags=["visual"]) for n in ["Minimal", "Bold", "Detailed", "Clean", "Geometric", "Soft", "Sharp", "Distressed", "Retro", "Gritty", "Polished", "Sketchy", "Painterly"]]

compositions = [create_entity(n, "cmp", tags=["layout"]) for n in ["Centered", "Asymmetrical", "Badge", "Circular Emblem", "Dynamic Diagonal", "Portrait", "Wide Scene", "Close-Up", "Rule of Thirds", "Golden Ratio", "Radial", "Isometric Grid", "Pattern"]]

palettes = [create_entity(n, "pal", tags=["color"]) for n in ["Halloween Night", "Retro Halloween", "Christmas Classic", "Neon", "Pastel", "Monochrome", "High Contrast", "Earth Tones", "Jewel Tones", "Muted", "Vibrant", "Grayscale", "Sepia", "Duotone", "Cyanotype", "Sunset", "Oceanic", "Forest Canopy"]]

decorations = [create_entity(n, "dec", tags=["detail"]) for n in ["Stars", "Moon", "Bats", "Skulls", "Spider Webs", "Pumpkins", "Snowflakes", "Flowers", "Lightning", "Gears", "Circuits", "Clouds", "Flames", "Sparks", "Leaves", "Vines", "Geometric Shapes", "Arrows", "Borders", "Sun", "Planets"]]

typography = [create_entity(n, "typ", tags=["font"]) for n in ["Bold Sans", "Retro Script", "Typewriter", "Blackletter", "Arcade", "Distressed", "Serif", "Handwritten", "Brush Script", "Stencil", "Bubble", "Western"]]

textures = [create_entity(n, "tex", tags=["surface"]) for n in ["Paper Grain", "Canvas", "Grunge", "Halftone", "Ink Bleed", "Wood", "Metal", "Concrete", "Chalk", "Paint Strokes", "Watercolor Paper"]]

visual_effects = [create_entity(n, "eff", tags=["fx"]) for n in ["Neon Glow", "Fog", "Sparks", "Motion Blur", "Lens Flare", "Chromatic Aberration", "Double Exposure", "Light Trails", "Silhouette", "Rim Light", "Volumetric Light", "Film Grain"]]

data = {
    "version": "2.0",
    "occasions": occasions,
    "themes": themes,
    "subjects": subjects,
    "actions": actions,
    "environments": environments,
    "moods": moods,
    "art_styles": art_styles,
    "visual_styles": vis_styles,
    "compositions": compositions,
    "palettes": palettes,
    "decorations": decorations,
    "typography": typography,
    "textures": textures,
    "visual_effects": visual_effects
}

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Generated {sum(len(v) for v in data.values() if isinstance(v, list))} semantically rich entities.")
