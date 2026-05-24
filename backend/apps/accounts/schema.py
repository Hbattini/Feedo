"""GraphQL account surface. Auth lifecycle stays in allauth Headless."""

import strawberry
from strawberry.types import Info


@strawberry.type
class Viewer:
    public_id: strawberry.ID
    email: str


@strawberry.type
class AccountsQuery:
    @strawberry.field
    def viewer(self, info: Info) -> Viewer | None:
        user = info.context.request.user
        if not user.is_authenticated:
            return None
        return Viewer(public_id=strawberry.ID(str(user.public_id)), email=user.email)


@strawberry.type
class AccountsMutation:
    @strawberry.field
    def auth_boundary(self) -> str:
        return "Auth mutations are provided by django-allauth Headless."
