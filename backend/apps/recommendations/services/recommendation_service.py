"""Database boundary for deterministic recommendation generation."""

from __future__ import annotations


def generate_for_cat(cat_public_id: str, limit: int = 10) -> dict:
    raise NotImplementedError("Recommendation persistence/read model implementation deferred.")
