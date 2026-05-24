"""Food catalog and ingestion models."""

from __future__ import annotations

from django.db import models

from apps.common.enums import CatalogStatus, FoodSource, TagSource, ValidationStatus
from apps.common.models import CreatedAtModel, TimeStampedModel, UUIDModel


class FoodRawSource(UUIDModel):
    source = models.CharField(max_length=32, choices=FoodSource.choices)
    external_id = models.CharField(max_length=180)
    source_url = models.URLField(blank=True)
    payload = models.JSONField()
    payload_hash = models.CharField(max_length=128, db_index=True)
    fetched_at = models.DateTimeField()
    validation_status = models.CharField(
        max_length=32,
        choices=ValidationStatus.choices,
        default=ValidationStatus.PENDING,
    )
    rejection_reason = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "external_id", "payload_hash"],
                name="unique_raw_food_payload",
            )
        ]


class Food(UUIDModel, TimeStampedModel):
    canonical_name = models.CharField(max_length=240)
    brand_name = models.CharField(max_length=160)
    external_ids = models.JSONField(default=dict, blank=True)
    chewy_url = models.URLField(blank=True)
    source_record = models.ForeignKey(
        FoodRawSource,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="foods",
    )
    catalog_status = models.CharField(
        max_length=32,
        choices=CatalogStatus.choices,
        default=CatalogStatus.INACTIVE,
    )

    class Meta:
        indexes = [
            models.Index(fields=["brand_name", "canonical_name"]),
            models.Index(fields=["catalog_status"]),
        ]

    def __str__(self) -> str:
        return f"{self.brand_name} {self.canonical_name}"


class FoodAttribute(UUIDModel, TimeStampedModel):
    food = models.OneToOneField(Food, on_delete=models.CASCADE, related_name="attributes")
    life_stage = models.ForeignKey("common.LifeStage", on_delete=models.PROTECT)
    texture = models.ForeignKey("common.Texture", on_delete=models.PROTECT, null=True, blank=True)
    primary_protein = models.ForeignKey(
        "common.Protein",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    is_wet = models.BooleanField(null=True, blank=True)
    protein_percent = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    fat_percent = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    moisture_percent = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    ingredient_text = models.TextField()
    feature_json = models.JSONField(default=dict, blank=True)
    data_source = models.CharField(max_length=32, choices=FoodSource.choices)
    last_synced_at = models.DateTimeField(null=True, blank=True)


class FoodNutritionalTag(UUIDModel, CreatedAtModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="nutritional_tags")
    nutritional_tag = models.ForeignKey("common.NutritionalTag", on_delete=models.PROTECT)
    source = models.CharField(max_length=32, choices=TagSource.choices)
    confidence = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["food", "nutritional_tag", "source"],
                name="unique_food_tag_source",
            )
        ]
