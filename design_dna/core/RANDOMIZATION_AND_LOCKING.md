# Randomness and Field Locking Architecture

This document explains the mathematical pipeline used to select elements (Subjects, Styles, etc.) in the Design DNA Generator, explaining how randomness is controlled via Temperature and how user-Locked Fields influence that randomness.

## 1. The Core Philosophy
The Design DNA generator doesn't use simple `random.choice()`. Instead, it uses a **Weighted Temperature Selection**.
When selecting a new field (e.g. "Subject"), it looks at the currently selected items (the "Context") and gives every available Subject a probability weight.

## 2. Compatibility Engine (The Scorer)
Before randomness occurs, every available item gets a base score (0.0 to 1.0) via the `CompatibilityEngine`:
*   `0.0`: Hard Incompatibility (e.g., Cyberpunk explicitly forbids Thanksgiving).
*   `0.5`: Neutral (No known relationship).
*   `0.65 to 0.95`: Intrinsic Affinity (They share tags like "spring", "cute" or have explicit preferred family ties in Ground Truth metadata).
*   `1.0`: Highly Compatible (Explicit rule or exact match).

To prevent dilution, the score an item receives is the **maximum** score it gets against *any* item currently in the Context. If you locked "Easter" (which loves "Rabbit" = 0.95), and the generator randomly picked a neutral "Pop Art" theme (which sees "Rabbit" as 0.5), the final score for Rabbit remains **0.95**.

## 3. The Temperature Randomizer (The Scale)
Once base scores are determined, the `TemperatureRandomizer` translates them into final probabilities using an exponential curve based on the user's `Temperature` (0-100) setting.

The issue with a large database (e.g., 300 Subjects) is "Probability Dilution". If a highly compatible item scores `0.95`, and 299 other neutral items score `0.5`, the combined weight of the neutral items mathematically drowns out the compatible item if we select linearly.

To fix this, the Randomizer applies an exponent (`power`) to the score:
*   **T = 0**: Pure Determinism. Only the absolute highest score is picked.
*   **T = 20 (power ~18.0)**: Extreme Bias. Highly compatible items (`0.95^18 = 0.39`) massively outweigh neutral items (`0.5^18 = 0.000003`). Related items are almost guaranteed.
*   **T = 50 (power = 8.0)**: Normal weighted distribution. `0.95^8 = 0.66`, `0.5^8 = 0.003`.
*   **T = 100 (power = 0.5)**: Exploratory/Wildcards. Flattens probabilities so even low-scoring (but valid) items have a chance. A score of `0.95^0.5 = 0.97` vs `0.5^0.5 = 0.70`. Hard zeroes (`0.0`) are still completely forbidden.

## 4. How Locked Fields Work (Context Anchors)
When a user "Locks" a field in the GUI (e.g., locking the Occasion to "Easter"), two things happen:

1.  **Pipeline Bypass:** The Generator skips the `randomizer.select_weighted` step for that specific category and injects the locked ID directly into the Design DNA.
2.  **Context Seeding:** Most importantly, the locked ID is immediately added to the `selected_ids` Context Array.

Because the Generator operates sequentially (Occasion -> Theme -> Subject -> Art Style -> etc.), the locked Occasion becomes the very first "Anchor". Every subsequent category chosen by the Generator is mathematically evaluated against that lock. Because of the `max()` scoring rule and the steep exponential temperature curve, locking a field exerts massive gravity over the rest of the generation, pulling conceptually related items out of the massive database pool to create a coherent design.
