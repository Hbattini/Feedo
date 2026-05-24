"""Hard filtering stage."""

from __future__ import annotations

from apps.recommendations.engine.context import CatRecommendationContext, FoodCandidate


def apply_hard_filters(
    context: CatRecommendationContext,
    candidates: list[FoodCandidate],
    required_tags_by_condition: dict[str, set[str]],
) -> list[FoodCandidate]:
    eligible: list[FoodCandidate] = []
    for candidate in candidates:
        if candidate.catalog_status != "active":
            continue
        if context.life_stage_code and candidate.life_stage_code != context.life_stage_code:
            continue
        missing_required_tag = False
        for condition_code in context.active_condition_codes:
            required_tags = required_tags_by_condition.get(condition_code, set())
            if not required_tags.issubset(candidate.nutritional_tag_codes):
                missing_required_tag = True
                break
        if missing_required_tag:
            continue
        eligible.append(candidate)
    return eligible
