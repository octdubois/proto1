import random
import math
from typing import List, Any, Callable

class TemperatureRandomizer:
    def __init__(self, seed: int = None):
        self.rng = random.Random(seed)
        self.seed = seed

    def set_seed(self, seed: int):
        self.seed = seed
        self.rng = random.Random(seed)

    def select_weighted(self, items: List[Any], weight_func: Callable[[Any], float], temperature: int) -> Any:
        """
        Selects an item based on weights adjusted by temperature (0-100).
        0 = Highly conservative (almost always picks highest weight)
        50 = Uses weights proportionally
        100 = Highly creative (flattens weights, approaching uniform distribution, but respects 0.0)
        """
        if not items:
            return None

        # Calculate raw weights
        weights = [weight_func(item) for item in items]

        # Filter out hard incompatibilities
        valid_pairs = [(item, w) for item, w in zip(items, weights) if w > 0.0]
        if not valid_pairs:
            # Fallback if nothing is compatible, pick uniformly from original items
            return self.rng.choice(items)

        valid_items, valid_weights = zip(*valid_pairs)

        if temperature == 0:
            # Deterministic max
            max_weight = max(valid_weights)
            best_items = [item for item, w in zip(valid_items, valid_weights) if w == max_weight]
            return self.rng.choice(best_items)

        # Normalize temperature to a continuous exponent (power)
        # T = 0   -> Highest compatibility strictly preferred (Handled above deterministically)
        # T = 50  -> power = 1.0 (Normal weighted probabilities)
        # T = 100 -> power = 0.1 (Flattens probabilities, exploratory, allows unusual/wildcards)

        if temperature < 50:
            # Scale 1-49 to exponent range [5.0 ... 1.0] (continuous)
            power = 1.0 + ((50 - temperature) / 50.0) * 4.0
        else:
            # Scale 50-100 to exponent range [1.0 ... 0.1] (continuous)
            power = 1.0 - ((temperature - 50) / 50.0) * 0.9

        adjusted_weights = [math.pow(w, power) for w in valid_weights]

        # Determine if we should allow a "wildcard" by injecting slight noise to low scores
        # at high temperatures, but hard zeros (w==0.0) are already filtered out.
        from .config import AppConfig
        wildcard_threshold = AppConfig().generation_limits.get("wildcard_threshold_temperature", 60)

        if temperature >= wildcard_threshold:
            # Flatten low weights slightly more to allow wildcard selections to have a realistic chance
            adjusted_weights = [w + 0.1 if w > 0 else 0 for w in adjusted_weights]

        return self.rng.choices(valid_items, weights=adjusted_weights, k=1)[0]
