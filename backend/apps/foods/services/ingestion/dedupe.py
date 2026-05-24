"""Conservative food dedupe helpers."""

from __future__ import annotations

from apps.foods.services.ingestion.normalize import NormalizedFoodInput


def dedupe_key(food: NormalizedFoodInput, package_size: str | None = None) -> tuple[str, str, str]:
    return (
        food.brand_name.casefold(),
        food.canonical_name.casefold(),
        (package_size or "").casefold(),
    )
