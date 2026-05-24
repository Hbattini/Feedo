"""Append-only cat event service boundary."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CatEventDraft:
    cat_public_id: str
    event_type_code: str
    occurred_at: datetime
    food_public_id: str | None = None
    recommendation_item_public_id: str | None = None
    source: str = "manual_log"
    metadata: dict[str, Any] = field(default_factory=dict)


def append_cat_event(draft: CatEventDraft, event_id: uuid.UUID | None = None) -> uuid.UUID:
    """Append one immutable event row and return its correlation event_id."""
    validate_event_metadata(draft.event_type_code, draft.metadata)
    raise NotImplementedError("Event append persistence will be implemented with the models.")


def append_cat_event_group(drafts: list[CatEventDraft], event_id: uuid.UUID | None = None) -> uuid.UUID:
    """Append a group of immutable event rows sharing one event_id."""
    group_id = event_id or uuid.uuid4()
    for draft in drafts:
        validate_event_metadata(draft.event_type_code, draft.metadata)
    raise NotImplementedError("Grouped event append persistence will be implemented with the models.")


def validate_event_metadata(event_type_code: str, metadata: dict[str, Any]) -> None:
    """Validate typed metadata per canonical event type."""
    allowed_keys_by_event = {
        "explicit_positive": {"onboarding_step", "preference_strength"},
        "explicit_negative": {"onboarding_step", "preference_strength"},
        "bowl_finished": {"portion_percent", "feeding_context"},
        "bowl_ignored": {"portion_percent", "feeding_context"},
        "vomited_after": {"delay_minutes", "user_note"},
        "recommendation_clicked": {"destination", "rank"},
        "recommendation_dismissed": {"rank", "reason"},
    }
    allowed_keys = allowed_keys_by_event.get(event_type_code)
    if allowed_keys is None:
        raise ValueError(f"Unsupported event type: {event_type_code}")
    unknown_keys = set(metadata) - allowed_keys
    if unknown_keys:
        raise ValueError(f"Unsupported metadata keys for {event_type_code}: {sorted(unknown_keys)}")
