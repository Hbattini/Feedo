"""Recommendation engine output shapes."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoredFood:
    food_public_id: str
    score: int
    matched_conditions: list[str] = field(default_factory=list)
    matched_preferences: list[str] = field(default_factory=list)
    positive_events: list[str] = field(default_factory=list)
    negative_events: list[str] = field(default_factory=list)
    exclusion_reasons: list[str] = field(default_factory=list)
    is_exploration: bool = False
