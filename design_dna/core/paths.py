import os
from pathlib import Path

# Get the absolute path of the design_dna root folder
BASE_DIR = Path(__file__).resolve().parent.parent

def get_data_path(filename: str) -> Path:
    return BASE_DIR / "data" / filename

def get_log_path(filename: str) -> Path:
    return BASE_DIR / "logs" / filename

def get_output_path() -> Path:
    return BASE_DIR / "output" / "dna"

def get_config_path(filename: str) -> Path:
    return BASE_DIR / "config" / filename
