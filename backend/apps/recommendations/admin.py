from django.contrib import admin

from apps.recommendations.models import (
    CatRecommendationState,
    ConditionTagMapping,
    GlobalRecommendationState,
    Recommendation,
    RecommendationFeedback,
    RecommendationItem,
)


@admin.register(ConditionTagMapping)
class ConditionTagMappingAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at", "updated_at")
    list_display = ("condition_code", "required_tag", "avoided_tag", "mapping_version", "is_active")
    list_filter = ("mapping_version", "is_active")


class RecommendationItemInline(admin.TabularInline):
    model = RecommendationItem
    readonly_fields = (
        "id",
        "public_id",
        "food",
        "rank",
        "score",
        "is_exploration",
        "explanation_payload",
        "exclusion_reasons",
        "created_at",
    )
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "cat", "rule_version", "generated_at", "cache_key", "metadata")
    list_display = ("cat", "rule_version", "generated_at")
    inlines = [RecommendationItemInline]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RecommendationFeedback)
class RecommendationFeedbackAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "public_id",
        "recommendation_item",
        "cat",
        "food",
        "event_id",
        "feedback_type",
        "metadata",
        "created_at",
    )
    list_display = ("cat", "food", "feedback_type", "created_at", "event_id")


@admin.register(CatRecommendationState)
class CatRecommendationStateAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at", "updated_at")
    list_display = ("cat", "recommendation_version", "updated_at")


@admin.register(GlobalRecommendationState)
class GlobalRecommendationStateAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at", "updated_at")
    list_display = ("key", "catalog_version", "updated_at")
