"""Recommendation cache invalidation service."""

from __future__ import annotations


def invalidate_cat_recommendations(cat_public_id: str) -> None:
    raise NotImplementedError("Per-cat recommendation version increment deferred.")


def invalidate_catalog_recommendations() -> None:
    raise NotImplementedError("Global catalog version increment deferred.")
