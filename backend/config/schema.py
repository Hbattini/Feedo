"""Root Strawberry schema composition."""

import strawberry

from apps.accounts.schema import AccountsMutation, AccountsQuery
from apps.cats.schema import CatsMutation, CatsQuery
from apps.foods.schema import FoodsMutation, FoodsQuery
from apps.recommendations.schema import RecommendationsMutation, RecommendationsQuery


@strawberry.type
class Query(AccountsQuery, CatsQuery, FoodsQuery, RecommendationsQuery):
    """Composed GraphQL query root."""


@strawberry.type
class Mutation(AccountsMutation, CatsMutation, FoodsMutation, RecommendationsMutation):
    """Composed GraphQL mutation root."""


schema = strawberry.Schema(query=Query, mutation=Mutation)
