"""Deterministic enrichment from normalized text to canonical taxonomy codes."""

from __future__ import annotations

CANONICAL_PROTEIN_KEYWORDS = {
    "chicken": "chicken",
    "tuna": "tuna",
    "salmon": "salmon",
    "turkey": "turkey",
    "beef": "beef",
    "duck": "duck",
    "rabbit": "rabbit",
}

CANONICAL_TEXTURE_KEYWORDS = {
    "pate": "pate",
    "shredded": "shredded",
    "chunks in gravy": "chunks_in_gravy",
    "minced": "minced",
    "mousse": "mousse",
    "kibble": "dry_kibble",
}


def infer_primary_protein(text: str) -> str | None:
    normalized = text.lower()
    for keyword, code in CANONICAL_PROTEIN_KEYWORDS.items():
        if keyword in normalized:
            return code
    return None


def infer_texture(text: str) -> str | None:
    normalized = text.lower()
    for keyword, code in CANONICAL_TEXTURE_KEYWORDS.items():
        if keyword in normalized:
            return code
    return None
