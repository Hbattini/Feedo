"""Cat profile, condition, measurement, and behavior event models."""

from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models

from apps.common.enums import ConditionSource, EventSource
from apps.common.models import CreatedAtModel, TimeStampedModel, UUIDModel


class Cat(UUIDModel, TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cats")
    household_id = models.UUIDField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=120)
    born_at = models.DateField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["owner", "name"])]

    def __str__(self) -> str:
        return self.name


class CatMeasurement(UUIDModel, CreatedAtModel):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name="measurements")
    measured_at = models.DateTimeField()
    weight_value = models.DecimalField(max_digits=7, decimal_places=2)
    weight_unit = models.CharField(max_length=12, default="lb")
    source = models.CharField(
        max_length=32,
        choices=ConditionSource.choices,
        default=ConditionSource.OWNER_REPORTED,
    )

    class Meta:
        indexes = [models.Index(fields=["cat", "-measured_at"])]


class CatCondition(UUIDModel, TimeStampedModel):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name="conditions")
    condition_code = models.ForeignKey("common.ConditionCode", on_delete=models.PROTECT)
    source = models.CharField(
        max_length=32,
        choices=ConditionSource.choices,
        default=ConditionSource.OWNER_REPORTED,
    )
    observed_at = models.DateField(null=True, blank=True)
    resolved_at = models.DateField(null=True, blank=True)
    veterinary_note = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=["cat", "resolved_at"])]


class CatEvent(UUIDModel, CreatedAtModel):
    event_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name="events")
    food = models.ForeignKey("foods.Food", on_delete=models.PROTECT, null=True, blank=True)
    recommendation_item = models.ForeignKey(
        "recommendations.RecommendationItem",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    event_type = models.ForeignKey("common.EventType", on_delete=models.PROTECT)
    occurred_at = models.DateTimeField()
    source = models.CharField(max_length=32, choices=EventSource.choices)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["cat", "-occurred_at"]),
            models.Index(fields=["food", "-occurred_at"]),
            models.Index(fields=["event_id"]),
            models.Index(fields=["event_type", "-occurred_at"]),
            models.Index(fields=["cat", "food", "event_type"]),
        ]
