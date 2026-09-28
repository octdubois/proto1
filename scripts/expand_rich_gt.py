import json
import uuid
from pathlib import Path
import random

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "design_dna" / "data" / "ground_truth.json"

def gen_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"

def create_entity(name, prefix, family=None, subcategory=None, tags=None, p_moods=None, p_styles=None, p_palettes=None):
    return {
        "id": gen_id(prefix),
        "name": name,
        "family": family,
        "subcategory": subcategory,
        "complexity": random.randint(1, 3),
        "tags": tags or [family.lower() if family else prefix],
        "characteristics": ["distinctive"],
        "preferred_moods": p_moods or [],
        "preferred_styles": p_styles or [],
        "preferred_palettes": p_palettes or [],
        "preferred_compositions": []
    }

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

def add_batch(category, items, prefix, family=None, subcategory=None):
    for item in items:
        data[category].append(create_entity(item, prefix, family, subcategory))

add_batch("occasions", ["Easter", "Thanksgiving", "Mother's Day", "Father's Day", "St. Patrick's Day", "Spring", "Autumn", "Winter", "Birthday", "Graduation", "Wedding", "Anniversary", "Retirement", "Camping Trip", "Road Trip", "Back to School", "Black Friday"], "occ", "Event")
add_batch("themes", ["Pirate", "Treasure Hunter", "Deep Sea", "Arctic Explorer", "Mountain Climber", "Desert Nomad", "Jungle Explorer", "Viking", "Samurai", "Ninja", "Gladiator", "Spartan"], "thm", "Adventure")
add_batch("themes", ["Baking", "Coffee Shop", "Brewery", "Pizzeria", "Sushi Bar", "Food Truck", "Farmers Market", "Candy Store"], "thm", "Food")

add_batch("subjects", ["Apple", "Banana", "Orange", "Strawberry", "Watermelon", "Grapes", "Pineapple", "Mango", "Peach", "Cherry", "Pizza", "Burger", "Hot Dog", "Taco", "Sushi", "Donut", "Ice Cream", "Cupcake", "Cookie", "Pancake"], "sub", "Food", "Edibles")
add_batch("subjects", ["Rose", "Tulip", "Sunflower", "Daisy", "Lily", "Orchid", "Cactus", "Succulent", "Bonsai", "Oak Tree", "Pine Tree", "Palm Tree", "Maple Tree", "Willow Tree"], "sub", "Nature", "Plants")
add_batch("subjects", ["Car", "Truck", "Motorcycle", "Bicycle", "Train", "Airplane", "Helicopter", "Boat", "Ship", "Submarine", "Rocket", "Hot Air Balloon"], "sub", "Vehicles", "Transport")
add_batch("subjects", ["Sword", "Shield", "Bow", "Arrow", "Axe", "Spear", "Dagger", "Mace", "Staff", "Wand", "Potion", "Scroll", "Grimoire", "Crystal"], "sub", "Fantasy", "Items")

add_batch("actions", ["Crawling", "Swimming", "Diving", "Climbing", "Falling", "Floating", "Sneaking", "Hiding", "Searching", "Hunting", "Gathering", "Crafting", "Building", "Repairing", "Cooking", "Baking", "Singing", "Playing Instrument", "Listening"], "act")

add_batch("environments", ["Coral Reef", "Deep Ocean", "Abyss", "Volcano", "Magma Chamber", "Tundra", "Glacier", "Ice Cave", "Oasis", "Savanna", "Rainforest", "Swamp", "Marsh", "Canyon", "Valley", "Meadow", "Prairie"], "env", "Nature")
add_batch("environments", ["Ruins", "Temple", "Pyramid", "Tomb", "Dungeon", "Labyrinth", "Colosseum", "Arena", "Tavern", "Inn", "Marketplace", "Bazaar", "Dock", "Harbor"], "env", "Historical")

add_batch("moods", ["Angry", "Furious", "Sad", "Sorrowful", "Lonely", "Isolated", "Anxious", "Nervous", "Excited", "Thrilled", "Bored", "Apathetic", "Confused", "Lost", "Determined", "Resolute", "Proud", "Confident", "Shy", "Timid"], "mod")

add_batch("art_styles", ["Fresco", "Mosaic", "Tapestry", "Embroidery", "Quilting", "Stained Glass", "Woodcut", "Linocut", "Engraving", "Etching", "Lithography", "Silk Screen", "Airbrush", "Graffiti", "Stencil Art", "Chalk Art", "Sand Art", "Ice Sculpture", "Origami", "Paper Mache"], "sty", "Traditional")
add_batch("art_styles", ["Glitch Art", "Vaporwave", "Synthwave", "Retrowave", "Outrun", "Seapunk", "Cyberprep", "Biopunk", "Nanopunk", "Raypunk", "Atompunk", "Cassette Futurism", "Y2K Aesthetic"], "sty", "Experimental")

add_batch("compositions", ["Grid", "Mosaic", "Collage", "Montage", "Triptych", "Diptych", "Polyptych", "Panoramic", "360 Degree", "Fish-eye", "Macro", "Microscopic", "Telescopic", "Bird's Eye", "Worm's Eye", "Dutch Angle", "Over the Shoulder", "Point of View"], "cmp")

add_batch("palettes", ["Primary Colors", "Secondary Colors", "Tertiary Colors", "Analogous", "Complementary", "Split Complementary", "Triadic", "Tetradic", "Square", "Monochromatic", "Achromatic", "Polychromatic", "Warm Tones", "Cool Tones", "Neutral Tones", "Pastel Tones", "Jewel Tones", "Earth Tones"], "pal")

add_batch("decorations", ["Circles", "Squares", "Triangles", "Polygons", "Hexagons", "Octagons", "Diamonds", "Crosses", "Spirals", "Waves", "Zigzags", "Dots", "Dashes", "Stripes", "Plaid", "Checkerboard", "Polka Dots", "Chevron", "Houndstooth", "Herringbone"], "dec")

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Expanded to {sum(len(v) for v in data.values() if isinstance(v, list))} semantically rich entities.")
