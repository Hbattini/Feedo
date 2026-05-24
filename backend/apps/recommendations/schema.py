"""GraphQL schema for recommendation workflows."""

import strawberry


@strawberry.type
class ExplanationPayload:
    matched_conditions: list[str]
    matched_preferences: list[str]
    positive_events: list[str]
    negative_events: list[str]
    confidence: float
    rule_version: str


@strawberry.type
class RecommendationItemType:
    public_id: strawberry.ID
    food_public_id: strawberry.ID
    rank: int
    score: float
    is_exploration: bool
    explanation_payload: ExplanationPayload


@strawberry.type
class RecommendationType:
    public_id: strawberry.ID
    cat_public_id: strawberry.ID
    rule_version: str
    generated_at: str
    items: list[RecommendationItemType]


@strawberry.input
class RecommendationFeedbackInput:
    recommendation_item_public_id: strawberry.ID
    cat_public_id: strawberry.ID
    feedback_event_type_code: str
    metadata: strawberry.scalars.JSON | None = None


@strawberry.type
class RecommendationsQuery:
    @strawberry.field
    def recommendations_for_cat(
        self,
        cat_public_id: strawberry.ID,
        limit: int = 10,
    ) -> RecommendationType | None:
        return None


@strawberry.type
class RecommendationsMutation:
    @strawberry.mutation
    def generate_recommendations_for_cat(
        self,
        cat_public_id: strawberry.ID,
        limit: int = 10,
    ) -> RecommendationType:
        raise NotImplementedError("Recommendation generation service is scaffolded but not implemented.")

    @strawberry.mutation
    def submit_recommendation_feedback(self, data: RecommendationFeedbackInput) -> strawberry.ID:
        raise NotImplementedError("Recommendation feedback service is scaffolded but not implemented.")
