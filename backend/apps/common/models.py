"""Shared base and taxonomy models."""

from __future__ import annotations

import uuid

from django.db import models


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TaxonomyBase(UUIDModel, TimeStampedModel):
    code = models.SlugField(max_length=80, unique=True)
    label = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["code"]

    def __str__(self) -> str:
        return self.code


class Protein(TaxonomyBase):
    pass


class Texture(TaxonomyBase):
    pass


class LifeStage(TaxonomyBase):
    min_age_months = models.PositiveIntegerField(null=True, blank=True)
    max_age_months = models.PositiveIntegerField(null=True, blank=True)


class NutritionalTag(TaxonomyBase):
    description = models.TextField(blank=True)


class ConditionCode(TaxonomyBase):
    is_supported = models.BooleanField(default=False)


class EventType(TaxonomyBase):
    signal_weight = models.IntegerField(null=True, blank=True)
