# Event Log Contract

## Decision

`cat_events` is an append-only behavioral event log.

## Row Semantics

- `id` uniquely identifies the event row.
- `event_id` groups related immutable rows from one submitted interaction.
- `occurred_at` is when the behavior happened.
- `created_at` is when Feedo stored the fact.

## Hard Rules

- Never update event rows.
- Never delete event rows.
- Do not add `updated_at`.
- Do not store derived preference conclusions as mutable truth.
- Validate metadata per event type before append.

## Grouping

The backend generates `event_id` by default. Clients may pass `event_id` only for explicit grouped workflows, such as one food offered to multiple cats.

## Recommendation Interaction

Recommendation feedback writes a feedback row and appends a correlated `cat_event` in the same transaction. Cache invalidation runs after commit.
