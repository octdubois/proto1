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

# Hit ~1000 with huge categorized specific lists
add_batch("subjects", ["Swordfish", "Marlin", "Tuna", "Salmon", "Trout", "Bass", "Catfish", "Carp", "Goldfish", "Koi", "Piranha", "Electric Eel", "Stingray", "Manta Ray", "Jellyfish", "Octopus", "Squid", "Cuttlefish", "Nautilus", "Crab", "Lobster", "Shrimp", "Barnacle", "Starfish", "Sea Urchin", "Sea Cucumber", "Sponge", "Coral", "Anemone", "Clam", "Oyster", "Mussel", "Scallop", "Snail", "Slug", "Worm", "Leech", "Centipede", "Millipede", "Spider", "Scorpion", "Tick", "Mite", "Beetle", "Butterfly", "Moth", "Ant", "Bee", "Wasp", "Fly", "Mosquito", "Dragonfly", "Grasshopper", "Cricket", "Cockroach", "Mantis", "Stick Insect", "Flea", "Louse", "Aphid", "Cicada", "Ladybug", "Firefly"], "sub", "Nature", "Animals")
add_batch("subjects", ["Violin", "Cello", "Double Bass", "Harp", "Flute", "Clarinet", "Oboe", "Bassoon", "Saxophone", "Trumpet", "Trombone", "French Horn", "Tuba", "Piano", "Harpsichord", "Organ", "Synthesizer", "Drum Kit", "Snare Drum", "Bass Drum", "Cymbals", "Timpani", "Xylophone", "Marimba", "Vibraphone", "Glockenspiel", "Tambourine", "Triangle", "Castanets", "Maracas", "Congas", "Bongos", "Djembe", "Tabla", "Sitar", "Banjo", "Mandolin", "Ukulele", "Lute", "Lyre", "Bagpipes", "Accordion", "Harmonica", "Kazoo"], "sub", "Objects", "Instruments")
add_batch("subjects", ["Hammer", "Screwdriver", "Wrench", "Pliers", "Saw", "Drill", "Tape Measure", "Level", "Square", "Chisel", "File", "Clamp", "Vise", "Anvil", "Trowel", "Shovel", "Rake", "Hoe", "Pitchfork", "Wheelbarrow", "Lawnmower", "Chainsaw", "Leaf Blower", "Snowblower", "Hose", "Sprinkler", "Watering Can", "Bucket", "Mop", "Broom", "Dustpan", "Vacuum Cleaner", "Iron", "Ironing Board", "Sewing Machine", "Needle", "Thread", "Scissors", "Pins", "Thimble", "Measuring Tape"], "sub", "Objects", "Tools")
add_batch("subjects", ["Sofa", "Armchair", "Chair", "Stool", "Bench", "Table", "Desk", "Bed", "Mattress", "Pillow", "Blanket", "Duvet", "Wardrobe", "Closet", "Dresser", "Chest of Drawers", "Nightstand", "Bookshelf", "Cabinet", "Cupboard", "Pantry", "Counter", "Sink", "Toilet", "Bathtub", "Shower", "Mirror", "Rug", "Carpet", "Curtains", "Blinds", "Lamp", "Chandelier", "Sconce", "Vase", "Picture Frame", "Clock", "Television", "Radio", "Computer", "Laptop", "Tablet", "Smartphone"], "sub", "Objects", "Furniture")

add_batch("environments", ["Living Room", "Dining Room", "Kitchen", "Bedroom", "Bathroom", "Hallway", "Stairs", "Attic", "Basement", "Garage", "Porch", "Patio", "Balcony", "Garden", "Yard", "Shed", "Greenhouse"], "env", "Domestic")
add_batch("environments", ["Office", "Cubicle", "Conference Room", "Break Room", "Reception", "Lobby", "Elevator", "Stairwell", "Corridor", "Restroom", "Cafeteria", "Gym", "Locker Room", "Pool", "Court", "Field", "Track", "Stadium", "Arena", "Theater", "Auditorium", "Cinema", "Museum", "Gallery", "Library", "Archive"], "env", "Public")
add_batch("environments", ["Hospital", "Clinic", "Pharmacy", "Laboratory", "Operating Room", "Ward", "Morgue", "Asylum", "Prison", "Cell", "Interrogation Room", "Courtroom", "Police Station", "Fire Station", "Military Base", "Bunker", "Silo", "Hangar", "Warehouse", "Factory", "Plant", "Refinery", "Mine", "Quarry", "Construction Site"], "env", "Institutional")

add_batch("art_styles", ["De Stijl", "Constructivism", "Suprematism", "Bauhaus", "Dada", "Surrealism", "Abstract Expressionism", "Color Field", "Hard-edge", "Op Art", "Minimalism", "Conceptual Art", "Performance Art", "Installation Art", "Video Art", "Digital Art", "Net Art", "Glitch Art", "Generative Art", "Fractal Art", "Algorithmic Art", "AI Art"], "sty", "Modern")

add_batch("compositions", ["High Key", "Low Key", "Chiaroscuro", "Tenebrism", "Sfumato", "Impasto", "Glazing", "Scumbling", "Drybrush", "Wet-on-wet", "Alla Prima", "Plein Air", "Grisaille", "Camaieu", "Trompe L'oeil", "Anamorphosis", "Foreshortening", "Linear Perspective", "Atmospheric Perspective", "Aerial Perspective"], "cmp")

add_batch("textures", ["Smooth", "Rough", "Bumpy", "Spiky", "Furry", "Hairy", "Feathery", "Scaly", "Slimy", "Sticky", "Wet", "Dry", "Cracked", "Peeling", "Flaking", "Crumbling", "Powdery", "Dusty", "Sandy", "Gritty", "Gravelly", "Rocky", "Stony", "Pebbly", "Cobbled", "Paved", "Asphalt", "Concrete", "Cement", "Brick", "Tile", "Slate", "Marble", "Granite", "Quartz", "Glass", "Crystal", "Gemstone", "Diamond", "Gold", "Silver", "Copper", "Bronze", "Brass", "Iron", "Steel", "Aluminum", "Titanium", "Plastic", "Rubber", "Silicone", "Latex", "Leather", "Suede", "Velvet", "Silk", "Satin", "Cotton", "Wool", "Linen", "Hemp", "Jute", "Burlap", "Canvas", "Denim", "Corduroy", "Fleece", "Felt", "Lace", "Netting", "Mesh", "Wire", "Chainmail", "Armor", "Scales", "Shell", "Bone", "Horn", "Antler", "Ivory", "Tooth", "Claw", "Nail", "Hair", "Skin", "Flesh", "Muscle", "Vein", "Blood", "Tear", "Sweat", "Saliva", "Mucus", "Pus", "Scab", "Scar", "Wrinkle", "Dimple", "Freckle", "Mole", "Wart", "Blister", "Pimple", "Rash", "Bruise", "Cut", "Scrape", "Burn", "Frostbite", "Sunburn", "Tan", "Pale", "Flush", "Blush"], "tex")

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Final Semantic Entities Count: {sum(len(v) for v in data.values() if isinstance(v, list))}")
