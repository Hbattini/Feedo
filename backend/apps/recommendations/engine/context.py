"""Typed inputs for the pure recommendation engine."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CatRecommendationContext:
    cat_public_id: str
    life_stage_code: str | None
    active_condition_codes: list[str]
    preferred_protein_codes: list[str] = field(default_factory=list)
    preferred_texture_codes: list[str] = field(default_factory=list)
    event_counts_by_food: dict[str, dict[str, int]] = field(default_factory=dict)


@dataclass(frozen=True)
class FoodCandidate:
    food_public_id: str
    life_stage_code: str
    protein_code: str | None
    texture_code: str | None
    nutritional_tag_codes: set[str]
    catalog_status: str
