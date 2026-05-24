"""GraphQL schema for cat workflows."""

from datetime import date, datetime

import strawberry


@strawberry.type
class CatType:
    public_id: strawberry.ID
    name: str
    born_at: date | None


@strawberry.input
class CreateCatProfileInput:
    name: str
    born_at: date | None = None


@strawberry.input
class LogCatEventInput:
    cat_public_id: strawberry.ID
    event_type_code: str
    occurred_at: datetime
    food_public_id: strawberry.ID | None = None
    event_id: strawberry.ID | None = None
    metadata: strawberry.scalars.JSON | None = None


@strawberry.type
class CatsQuery:
    @strawberry.field
    def my_cats(self) -> list[CatType]:
        return []

    @strawberry.field
    def cat(self, public_id: strawberry.ID) -> CatType | None:
        return None


@strawberry.type
class CatsMutation:
    @strawberry.mutation
    def create_cat_profile(self, data: CreateCatProfileInput) -> CatType:
        raise NotImplementedError("Cat profile creation service is scaffolded but not implemented.")

    @strawberry.mutation
    def log_cat_event(self, data: LogCatEventInput) -> strawberry.ID:
        raise NotImplementedError("Append-only event service is scaffolded but not implemented.")
