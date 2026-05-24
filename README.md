# Feedo

Feedo is a web app for deterministic, personalized cat food recommendations in multi-cat households.

The MVP architecture prioritizes:

- zero-cost open source tooling
- deterministic recommendation rules
- append-only behavioral events
- canonical taxonomies
- future ML-compatible data shape
- explanation-only LLM usage

## Architecture

- [MVP Architecture Plan](docs/architecture/mvp-architecture-plan.md)
- [Auth Contract](docs/architecture/decisions/auth-contract.md)
- [Domain Taxonomy](docs/architecture/decisions/domain-taxonomy.md)
- [Event Log Contract](docs/architecture/decisions/event-log-contract.md)
- [Recommendation Contract](docs/architecture/decisions/recommendation-contract.md)
- [Ingestion Pipeline](docs/architecture/decisions/ingestion-pipeline.md)

## Project Layout

```txt
backend/   Django, Strawberry GraphQL, allauth Headless
frontend/  React, TypeScript, Apollo Client, React Router
infra/     Docker Compose, PostgreSQL, Redis
docs/      Architecture plans and decision records
```

## Local Development

Copy environment examples before running services:

```txt
backend/.env.example -> backend/.env
frontend/.env.example -> frontend/.env
```

The Docker Compose scaffold is in `infra/docker-compose.yml`.
