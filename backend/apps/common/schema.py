"""Shared GraphQL types."""

import strawberry


@strawberry.type
class DomainError:
    code: str
    message: str
    field: str | None = None


@strawberry.type
class TaxonomyValue:
    public_id: strawberry.ID
    code: str
    label: str
    is_active: bool
