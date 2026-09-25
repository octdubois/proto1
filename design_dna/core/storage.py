import json
import os
from pathlib import Path
from .models import DesignDNA

from .paths import get_output_path, get_log_path

class StorageEngine:
    def __init__(self, json_dir: str = None, log_path: str = None):
        if json_dir is None:
            self.json_dir = get_output_path()
        else:
            self.json_dir = Path(json_dir)

        if log_path is None:
            self.log_path = get_log_path("creation_log.jsonl")
        else:
            self.log_path = Path(log_path)

        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _get_next_filename(self) -> str:
        """Finds the next sequential filename DNA-XXXXXX.json"""
        existing_files = list(self.json_dir.glob("DNA-*.json"))
        max_num = 0
        for f in existing_files:
            try:
                num = int(f.stem.split("-")[1])
                max_num = max(max_num, num)
            except (IndexError, ValueError):
                continue
        return f"DNA-{max_num + 1:06d}.json"

    def save_dna(self, dna: DesignDNA) -> str:
        filename = self._get_next_filename()
        filepath = self.json_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(dna.model_dump_json(indent=4))

        return filename

    def log_creation(self, dna: DesignDNA, filename: str):
        log_entry = {
            "design_id": dna.generation.id,
            "timestamp": dna.generation.timestamp,
            "seed": dna.generation.seed,
            "temperature": dna.generation.temperature,
            "filename": filename,
            "occasion": dna.context.occasion,
            "theme": dna.context.theme,
            "subject": dna.design.subject,
            "art_style": dna.design.art_style,
            "compatibility_score": dna.validation.compatibility_score,
            "novelty_score": dna.validation.novelty_score
        }

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
