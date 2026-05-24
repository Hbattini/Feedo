"""Recommendation audit, feedback, and freshness models."""

from __future__ import annotations

from django.db import models

from apps.common.models import TimeStampedModel, UUIDModel


class ConditionTagMapping(UUIDModel, TimeStampedModel):
    condition_code = models.ForeignKey("common.ConditionCode", on_delete=models.PROTECT)
    required_tag = models.ForeignKey(
        "common.NutritionalTag",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="required_by_condition_mappings",
    )
    avoided_tag = models.ForeignKey(
        "common.NutritionalTag",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="avoided_by_condition_mappings",
    )
    mapping_version = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["condition_code", "mapping_version", "is_active"])]


class Recommendation(UUIDModel):
    cat = models.ForeignKey("cats.Cat", on_delete=models.CASCADE, related_name="recommendations")
    rule_version = models.CharField(max_length=40)
    generated_at = models.DateTimeField()
    cache_key = models.CharField(max_length=300, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["cat", "-generated_at"])]


class RecommendationItem(UUIDModel):
    recommendation = models.ForeignKey(
        Recommendation,
        on_delete=models.CASCADE,
        related_name="items",
    )
    food = models.ForeignKey("foods.Food", on_delete=models.PROTECT)
    rank = models.PositiveIntegerField()
    score = models.DecimalField(max_digits=8, decimal_places=3)
    is_exploration = models.BooleanField(default=False)
    explanation_payload = models.JSONField(default=dict, blank=True)
    exclusion_reasons = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recommendation", "rank"],
                name="unique_recommendation_rank",
            )
        ]
        indexes = [models.Index(fields=["recommendation", "rank"])]


class RecommendationFeedback(UUIDModel):
    recommendation_item = models.ForeignKey(
        RecommendationItem,
        on_delete=models.PROTECT,
        related_name="feedbacks",
    )
    cat = models.ForeignKey("cats.Cat", on_delete=models.CASCADE)
    food = models.ForeignKey("foods.Food", on_delete=models.PROTECT)
    event_id = models.UUIDField(db_index=True)
    feedback_type = models.ForeignKey("common.EventType", on_delete=models.PROTECT)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CatRecommendationState(UUIDModel, TimeStampedModel):
    cat = models.OneToOneField("cats.Cat", on_delete=models.CASCADE, related_name="recommendation_state")
    recommendation_version = models.PositiveIntegerField(default=1)


class GlobalRecommendationState(UUIDModel, TimeStampedModel):
    key = models.CharField(max_length=60, unique=True, default="global")
    catalog_version = models.PositiveIntegerField(default=1)
