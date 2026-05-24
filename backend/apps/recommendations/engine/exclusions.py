"""Exclusion stage."""

from __future__ import annotations

from apps.recommendations.engine.constants import HARD_EXCLUSION_EVENT_TYPES
from apps.recommendations.engine.context import CatRecommendationContext, FoodCandidate


def apply_exclusions(
    context: CatRecommendationContext,
    candidates: list[FoodCandidate],
    avoided_tags: set[str],
) -> list[FoodCandidate]:
    retained: list[FoodCandidate] = []
    for candidate in candidates:
        event_counts = context.event_counts_by_food.get(candidate.food_public_id, {})
        if any(event_counts.get(event_type, 0) > 0 for event_type in HARD_EXCLUSION_EVENT_TYPES):
            continue
        if candidate.nutritional_tag_codes.intersection(avoided_tags):
            continue
        retained.append(candidate)
    return retained
