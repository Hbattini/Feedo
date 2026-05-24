"""Additive scoring stage."""

from __future__ import annotations

from apps.recommendations.engine.constants import MAX_SCORE, SCORES
from apps.recommendations.engine.context import CatRecommendationContext, FoodCandidate
from apps.recommendations.engine.result import ScoredFood


def score_candidate(context: CatRecommendationContext, candidate: FoodCandidate) -> ScoredFood:
    score = 0
    matched_preferences: list[str] = []
    positive_events: list[str] = []
    negative_events: list[str] = []

    if context.life_stage_code == candidate.life_stage_code:
        score += SCORES["life_stage_match"]

    if candidate.protein_code and candidate.protein_code in context.preferred_protein_codes:
        score += SCORES["preferred_protein"]
        matched_preferences.append(candidate.protein_code)

    if candidate.texture_code and candidate.texture_code in context.preferred_texture_codes:
        score += SCORES["preferred_texture"]
        matched_preferences.append(candidate.texture_code)

    event_counts = context.event_counts_by_food.get(candidate.food_public_id, {})
    if event_counts.get("bowl_finished", 0):
        score += SCORES["bowl_finished"] * event_counts["bowl_finished"]
        positive_events.append("bowl_finished")
    if event_counts.get("bowl_ignored", 0):
        score += SCORES["bowl_ignored"] * event_counts["bowl_ignored"]
        negative_events.append("bowl_ignored")

    return ScoredFood(
        food_public_id=candidate.food_public_id,
        score=min(score, MAX_SCORE),
        matched_preferences=matched_preferences,
        positive_events=positive_events,
        negative_events=negative_events,
    )


def score_candidates(
    context: CatRecommendationContext,
    candidates: list[FoodCandidate],
) -> list[ScoredFood]:
    return [score_candidate(context, candidate) for candidate in candidates]
