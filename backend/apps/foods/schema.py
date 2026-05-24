"""GraphQL schema for food catalog reads."""

import strawberry


@strawberry.type
class FoodType:
    public_id: strawberry.ID
    canonical_name: str
    brand_name: str
    chewy_url: str | None


@strawberry.type
class FoodsQuery:
    @strawberry.field
    def food(self, public_id: strawberry.ID) -> FoodType | None:
        return None

    @strawberry.field
    def food_catalog(self, first: int = 20, after: str | None = None) -> list[FoodType]:
        return []


@strawberry.type
class FoodsMutation:
    @strawberry.field
    def food_mutation_boundary(self) -> str:
        return "Food writes are owned by ingestion commands, not public GraphQL mutations."
