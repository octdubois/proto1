import json
from pathlib import Path
from .models import GroundTruthModel

from .paths import get_data_path

class GroundTruth:
    def __init__(self, file_path: str = None):
        if file_path is None:
            self.file_path = get_data_path("ground_truth.json")
        else:
            self.file_path = Path(file_path)
        self.data: GroundTruthModel = self._load()

    def _load(self) -> GroundTruthModel:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Ground Truth file not found at {self.file_path}")

        with open(self.file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        return GroundTruthModel(**raw_data)

    def get_entities(self, category: str):
        """Returns a list of Entity objects for a given category."""
        return getattr(self.data, category, [])

    def get_entity(self, category: str, entity_id: str):
        """Returns a specific Entity by ID, or None if not found."""
        entities = self.get_entities(category)
        for entity in entities:
            if entity.id == entity_id:
                return entity
        return None

    def validate_reference(self, category: str, entity_id: str) -> bool:
        """Check if an entity ID exists in a category."""
        return self.get_entity(category, entity_id) is not None
