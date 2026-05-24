"""Seeded deterministic exploration injection."""

from __future__ import annotations

import random
from dataclasses import replace

from apps.recommendations.engine.constants import EXPLOITATION_RATIO
from apps.recommendations.engine.result import ScoredFood


def inject_exploration(
    ranked_foods: list[ScoredFood],
    *,
    limit: int,
    seed: str,
) -> list[ScoredFood]:
    if limit <= 0:
        return []
    exploitation_count = max(1, int(limit * EXPLOITATION_RATIO))
    exploration_count = max(0, limit - exploitation_count)
    exploitation = ranked_foods[:exploitation_count]
    exploration_pool = ranked_foods[exploitation_count:]
    rng = random.Random(seed)
    exploration = rng.sample(exploration_pool, min(exploration_count, len(exploration_pool)))
    marked_exploration = [replace(food, is_exploration=True) for food in exploration]
    return (exploitation + marked_exploration)[:limit]
