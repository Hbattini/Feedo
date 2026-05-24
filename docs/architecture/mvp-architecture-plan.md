# Feedo MVP Architecture Plan

## Summary

Feedo is scaffolded as a monorepo with separate backend, frontend, infra, and docs areas. The backend uses Django, Strawberry GraphQL, PostgreSQL, Redis, and `django-allauth[headless]` for mature auth. The frontend uses React, TypeScript, Apollo Client, React Router v6, shadcn/ui-ready folders, and GraphQL codegen placeholders.

Product and domain data stays GraphQL-only. Auth is the one intentional non-GraphQL exception through allauth Headless endpoints.

## Project Structure

```txt
Feedo/
  backend/
    config/
    apps/
      accounts/
      cats/
      foods/
      recommendations/
      common/
  frontend/
    src/
      app/
      components/
      features/
      graphql/
      routes/
      types/
  infra/
  docs/
```

## Backend Contracts

- Use a custom `accounts.User` from the first migration.
- Use seeded canonical taxonomy lookup tables for proteins, textures, life stages, nutritional tags, condition codes, and event types.
- Persist raw OPFF payloads separately from normalized food records.
- Keep `cat_events` append-only with a unique row `id` and shared grouping `event_id`.
- Validate event metadata per event type before writing.
- Keep veterinary notes optional and outside recommendation logic.
- Store recommendation outputs as audit snapshots, not mutable truth.

## Recommendation Contract

The rules engine is authoritative and deterministic:

1. hard filters
2. exclusions
3. additive scoring
4. ranking
5. seeded exploration injection
6. structured explanation payload generation

MVP rule weights live in code constants with `RULE_VERSION = "rules_v1"`. `vomited_after` is a hard exclusion. Exploration is deterministic and uses a stable seed from cat, rule version, and recommendation window.

LLMs receive structured explanation payloads only and cannot override filters, exclusions, scores, or ranks.

## Caching And Ingestion

Redis caches GraphQL-ready recommendation payload snapshots. Cache keys include cat public ID, rule version, per-cat recommendation version, global catalog version, and limit. Invalidation increments version tokens after the database transaction commits.

OPFF ingestion runs through Django management commands. Ingestion stores raw payloads, normalizes, validates, enriches deterministically, dedupes, persists accepted records, regenerates feature JSON, and increments the catalog version. Records with missing or unmappable life stage are rejected from the active catalog.

## Frontend Contracts

- Apollo Client owns GraphQL server state.
- Auth state lives in `AuthProvider` and talks to allauth Headless helpers.
- Multi-step onboarding uses `useReducer`.
- GraphQL codegen owns strict operation types.
- UI flows must keep cat context explicit for all feedback and recommendation actions.

## Verification Expectations

- Backend config/import checks should pass once dependencies are installed.
- Frontend strict TypeScript checks should pass once dependencies are installed.
- Docker Compose config should validate.
- Scaffold is not expected to implement full product behavior.
