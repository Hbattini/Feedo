"""Normalize untrusted food payloads into deterministic input records."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedFoodInput:
    external_id: str
    brand_name: str
    canonical_name: str
    ingredient_text: str
    source_url: str


def normalize_brand(value: str) -> str:
    return " ".join(value.strip().split()).title()


def normalize_product_name(value: str) -> str:
    return " ".join(value.strip().split())
