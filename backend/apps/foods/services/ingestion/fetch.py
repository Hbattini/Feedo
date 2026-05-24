"""OPFF fetch boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RawFoodPayload:
    source: str
    external_id: str
    source_url: str
    payload: dict[str, Any]


def fetch_opff_cat_foods(limit: int = 500) -> list[RawFoodPayload]:
    raise NotImplementedError("OPFF network fetch will be implemented after scaffold review.")
