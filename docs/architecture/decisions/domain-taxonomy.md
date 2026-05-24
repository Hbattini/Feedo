# Domain Taxonomy

## Decision

Canonical domain values are stored in lookup tables with stable `code` fields.

## Covered Taxonomies

- proteins
- textures
- life stages
- nutritional tags
- condition codes
- event types

## Rules

- No freeform internal strings for recommendation logic.
- Unsupported conditions can be recorded but must not affect recommendations.
- Frontend labels should come from GraphQL taxonomy data or generated types, not hand-maintained duplicate enums.

## Rationale

Lookup tables are more explicit, queryable, and ML-friendly than scattered code constants or frontend-only enums.
