"""Food validation rules for active catalog eligibility."""

from __future__ import annotations

from dataclasses import dataclass

from apps.foods.services.ingestion.normalize import NormalizedFoodInput


@dataclass(frozen=True)
class ValidationResult:
    accepted: bool
    rejection_reason: str = ""


def validate_normalized_food(food: NormalizedFoodInput, life_stage_code: str | None) -> ValidationResult:
    if not food.canonical_name:
        return ValidationResult(False, "missing_product_name")
    if not food.brand_name:
        return ValidationResult(False, "missing_brand_name")
    if not food.ingredient_text:
        return ValidationResult(False, "missing_ingredients")
    if not life_stage_code:
        return ValidationResult(False, "missing_or_unmapped_life_stage")
    return ValidationResult(True)
