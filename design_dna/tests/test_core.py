import pytest
import os
import sys

# Ensure module path is correct for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.ground_truth import GroundTruth
from core.compatibility import CompatibilityEngine
from core.randomizer import TemperatureRandomizer
from core.novelty import NoveltyEngine

class DummyEntity:
    def __init__(self, id):
        self.id = id

def test_ground_truth_loading():
    gt = GroundTruth()
    assert len(gt.data.occasions) > 0
    assert gt.validate_reference("occasions", "occ_halloween") == True
    assert gt.validate_reference("occasions", "invalid_id") == False

def test_compatibility_engine():
    ce = CompatibilityEngine()
    # Explicit rules
    assert ce.get_score("occ_halloween", "sub_black_cat") == 1.0
    # Missing rules default to 0.5
    assert ce.get_score("occ_general", "sub_black_cat") == 0.5

    # Aggregation
    assert ce.calculate_aggregate_score("sty_gothic", ["occ_halloween", "sub_black_cat"]) > 0.9

def test_temperature_randomizer():
    tr = TemperatureRandomizer(seed=42)
    items = [DummyEntity("A"), DummyEntity("B"), DummyEntity("C")]

    def weight_func(i):
        if i.id == "A": return 1.0
        if i.id == "B": return 0.5
        if i.id == "C": return 0.1

    # At temp=0, should always pick highest weight
    assert tr.select_weighted(items, weight_func, 0).id == "A"

def test_novelty_engine():
    ne = NoveltyEngine()
    ne.history = [] # clear for test

    d1 = {"subject": "sub_black_cat", "art_style": "sty_gothic"}
    d2 = {"subject": "sub_black_cat", "art_style": "sty_gothic"}
    d3 = {"subject": "sub_robot", "art_style": "sty_cyberpunk"}

    ne.add_to_history(d1)

    # Duplicate
    assert ne.evaluate_novelty(d2) == 0.0
    # Novel
    assert ne.evaluate_novelty(d3) == 1.0

if __name__ == "__main__":
    pytest.main(["-v", __file__])
