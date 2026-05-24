"""Persistence boundary for accepted normalized foods."""

from __future__ import annotations

from apps.foods.services.ingestion.normalize import NormalizedFoodInput


def persist_normalized_food(food: NormalizedFoodInput) -> None:
    raise NotImplementedError("Food persistence will be implemented with ingestion models.")
