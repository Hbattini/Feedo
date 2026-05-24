"""Redis recommendation cache boundary."""

from __future__ import annotations


def build_recommendation_cache_key(
    *,
    cat_public_id: str,
    rule_version: str,
    cat_version: int,
    catalog_version: int,
    limit: int,
) -> str:
    return (
        "feedo:recommendations:"
        f"{cat_public_id}:{rule_version}:{cat_version}:{catalog_version}:{limit}"
    )


def get_cached_recommendations(cache_key: str) -> dict | None:
    raise NotImplementedError("Redis read implementation deferred.")


def set_cached_recommendations(cache_key: str, payload: dict, ttl_seconds: int = 86400) -> None:
    raise NotImplementedError("Redis write implementation deferred.")
