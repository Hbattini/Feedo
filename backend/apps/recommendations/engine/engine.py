"""Pure recommendation engine orchestration."""

from __future__ import annotations

from apps.recommendations.engine.context import CatRecommendationContext, FoodCandidate
from apps.recommendations.engine.exclusions import apply_exclusions
from apps.recommendations.engine.exploration import inject_exploration
from apps.recommendations.engine.filters import apply_hard_filters
from apps.recommendations.engine.ranking import rank_scored_foods
from apps.recommendations.engine.result import ScoredFood
from apps.recommendations.engine.scoring import score_candidates


def generate_recommendations(
    *,
    context: CatRecommendationContext,
    candidates: list[FoodCandidate],
    required_tags_by_condition: dict[str, set[str]],
    avoided_tags: set[str],
    limit: int,
    seed: str,
) -> list[ScoredFood]:
    filtered = apply_hard_filters(context, candidates, required_tags_by_condition)
    retained = apply_exclusions(context, filtered, avoided_tags)
    scored = score_candidates(context, retained)
    ranked = rank_scored_foods(scored)
    return inject_exploration(ranked, limit=limit, seed=seed)
