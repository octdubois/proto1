# Design DNA Generator - System Documentation

## 1. Overview
The **Design DNA Generator** is a senior-level, modular Python application utilizing PyQt6. Its purpose is to programmatically generate structured JSON specifications (called "Design DNA") for merchandise-oriented artwork (e.g., t-shirts, stickers, posters).

It does **not** generate images directly. It acts as an ontological engine, structuring concepts that can later be parsed by an AI-image generator or production team.

## 2. Core Architectural Philosophy
**"Do not mix knowledge, rules, and generation."**

The system strictly enforces the separation of concerns across four pillars:
1.  **Ground Truth (Knowledge)**: Defines *what exists* in the universe.
2.  **Compatibility Engine (Rules)**: Defines *how well things work together*.
3.  **Generator & Randomizer (Execution)**: Orchestrates the pipeline and mathematically scales probabilities based on the desired creativity (Temperature).
4.  **Validator & Novelty (Constraint Enforcement)**: Ensures structural integrity and prevents duplicate generations.

## 3. The Data Layer (Ground Truth)
Located in `data/ground_truth.json`.
It contains over 1,000 semantically rich entities divided into categories:
*   `occasions`, `themes`, `subjects`, `actions`, `environments`, `moods`, `art_styles`, `visual_styles`, `compositions`, `palettes`, `decorations`, `typography`, `textures`, `visual_effects`.

Every entity holds metadata defining its characteristics and intrinsic affinities. Example:
```json
{
  "id": "sub_dccb68",
  "name": "Rabbit",
  "tags": ["spring", "cute", "rabbit"],
  "preferred_styles": ["Illustration", "Kawaii"]
}
```

## 4. The Rules Layer (Compatibility Engine)
Located in `core/compatibility.py` and `data/compatibility_rules.json`.
When the Generator asks "How compatible is X with Y?", the engine evaluates:
1.  **Authoritative Rules:** Checks `compatibility_rules.json` for explicit manual rules (e.g., Score = `0.0` or `1.0`). Directional rules (X->Y) take precedence over symmetric rules (X<->Y).
2.  **Intrinsic Fallback:** If no rule exists, it dynamically calculates an affinity score (0.5 to 1.0) by analyzing the semantic overlap in the Ground Truth (e.g., Do they share tags? Does one prefer the other's family?).

*Note: Hard Incompatibilities (`0.0`) are unconditionally preserved.*

## 5. The Execution Layer (Generator & Randomizer)
Located in `core/generator.py` and `core/randomizer.py`.
The generation pipeline follows a strict, sequential 22-step process, beginning with Occasion and Theme, and cascading down through Subjects, Styles, Compositions, and Visual Effects.

### 5.1 Bias Toward Merchandise
The generator heavily biases weighting toward merchandise-friendly graphics (e.g., Vector Art, Badges) while actively suppressing complex photographic or environmental scenes.

### 5.2 Context Anchors (Locking)
If a user "Locks" a field in the GUI, it becomes an anchor. The Compatibility Engine uses the `max()` score against all anchors to prevent the influence of strong relationships from being mathematically diluted by subsequent neutral selections.

### 5.3 Temperature
The `TemperatureRandomizer` transforms base compatibility scores into selection probabilities using continuous exponentiation.
*   **Low Temp (< 50)**: Applies steep exponents (e.g., power 15.0). Neutral options vanish statistically. High compatibility is practically guaranteed.
*   **High Temp (> 50)**: Flattens exponents. Unusual combinations ("wildcards") are permitted.

*For detailed math, refer to `core/RANDOMIZATION_AND_LOCKING.md`.*

## 6. Constraints Layer (Validation & Novelty)
*   **Validator**: Checks the assembled Design DNA for hard incompatibilities. If detected, it fails.
*   **NoveltyEngine**: Stores every generation in `logs/creation_log.jsonl`. New designs are weighted against historical designs. If a design hits a similarity threshold (e.g., >85% identical), it is rejected as a Near Duplicate based on the user's `config/generator_config.json` settings.

## 7. Configuration & GUI
*   **GUI (`gui/main_window.py`)**: Built with PyQt6. Features generation controls, field locking, JSON output with an editor and validation, and a double-clickable historical log.
*   **Config (`config/generator_config.json`)**: Dictates default temperatures, minimum/maximum limits for secondary subjects, wildcard thresholds, and duplicate detection toggles.
