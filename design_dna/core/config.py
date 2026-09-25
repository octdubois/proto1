import json
from .paths import get_config_path

class AppConfig:
    def __init__(self):
        self.config_path = get_config_path("generator_config.json")
        self.settings = self._load()

    def _load(self):
        if not self.config_path.exists():
            return {
                "default_temperature": 50,
                "duplicate_detection": {
                    "avoid_exact": True,
                    "avoid_near": False,
                    "near_duplicate_threshold": 0.85
                }
            }
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def default_temperature(self):
        return self.settings.get("default_temperature", 50)

    @property
    def duplicate_detection(self):
        return self.settings.get("duplicate_detection", {})
