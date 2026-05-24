"""Ranking stage."""

from __future__ import annotations

from apps.recommendations.engine.result import ScoredFood


def rank_scored_foods(scored_foods: list[ScoredFood]) -> list[ScoredFood]:
    return sorted(scored_foods, key=lambda food: (-food.score, food.food_public_id))
