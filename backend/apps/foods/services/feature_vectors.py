"""Feature JSON generation from canonical food attributes."""

from __future__ import annotations


def build_feature_json(
    *,
    is_wet: bool | None,
    protein_code: str | None,
    texture_code: str | None,
    life_stage_code: str,
    nutritional_tag_codes: list[str],
) -> dict[str, int]:
    feature_json: dict[str, int] = {}
    if is_wet is not None:
        feature_json["is_wet"] = int(is_wet)
    if protein_code:
        feature_json[f"protein_{protein_code}"] = 1
    if texture_code:
        feature_json[f"texture_{texture_code}"] = 1
    feature_json[f"life_stage_{life_stage_code}"] = 1
    for code in nutritional_tag_codes:
        feature_json[f"tag_{code}"] = 1
    return feature_json
