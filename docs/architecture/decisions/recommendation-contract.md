# Recommendation Contract

## Decision

The MVP recommendation engine is deterministic and rules-based. It does not use ML, embeddings, or vector databases.

## Flow

1. hard filters
2. exclusions
3. additive scoring
4. ranking
5. seeded exploration injection
6. explanation payload generation

## Rules

- Hard filters and exclusions happen before scoring.
- Exploration can only select eligible foods.
- `vomited_after` is a hard exclusion.
- Rule weights live in code constants for MVP.
- Recommendation rows are audit snapshots, not mutable truth.

## LLM Boundary

LLMs receive structured explanation payloads only. They must not invent medical claims, unsupported nutrition logic, or unmapped condition reasoning.
