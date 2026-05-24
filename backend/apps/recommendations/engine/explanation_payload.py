"""Structured explanation payload generation."""

from __future__ import annotations

from apps.recommendations.engine.constants import RULE_VERSION
from apps.recommendations.engine.result import ScoredFood


def build_explanation_payload(scored_food: ScoredFood) -> dict[str, object]:
    confidence = max(0.0, min(scored_food.score / 100, 1.0))
    return {
        "matched_conditions": scored_food.matched_conditions,
        "matched_preferences": scored_food.matched_preferences,
        "positive_events": scored_food.positive_events,
        "negative_events": scored_food.negative_events,
        "confidence": confidence,
        "rule_version": RULE_VERSION,
    }
