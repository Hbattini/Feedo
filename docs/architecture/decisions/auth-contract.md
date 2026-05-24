# Auth Contract

## Decision

Feedo uses `django-allauth[headless]` for authentication and account lifecycle. Auth endpoints are the only intentional exception to the product API's GraphQL-only rule.

## Boundaries

- allauth Headless owns signup, login, logout, email flows, session/token mechanics, and password reset.
- GraphQL exposes product/domain data and a `viewer` query.
- Frontend auth helpers are isolated in `features/auth` and do not leak REST patterns into product features.

## Rationale

Auth is security-sensitive. A mature Django package is preferred over a custom JWT implementation for the MVP.

## Constraints

- Do not store tokens in `localStorage`.
- Product GraphQL mutations must require authenticated users where appropriate.
- `accounts.User` must be the custom user model from the first migration.
