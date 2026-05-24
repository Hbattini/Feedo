"""Canonical codes used by deterministic domain logic."""

from __future__ import annotations

from django.db import models


class FoodSource(models.TextChoices):
    OPFF = "opff", "Open Pet Food Facts"
    CHEWY_FEED = "chewy_feed", "Chewy Feed"
    MANUAL_SEED = "manual_seed", "Manual Seed"


class ConditionSource(models.TextChoices):
    OWNER_REPORTED = "owner_reported", "Owner Reported"
    VETERINARY_RECORD = "veterinary_record", "Veterinary Record"
    IMPORTED_RECORD = "imported_record", "Imported Record"


class EventSource(models.TextChoices):
    ONBOARDING = "onboarding", "Onboarding"
    RECOMMENDATION = "recommendation", "Recommendation"
    MANUAL_LOG = "manual_log", "Manual Log"
    IMPORT = "import", "Import"


class CatalogStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    REJECTED = "rejected", "Rejected"


class ValidationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class TagSource(models.TextChoices):
    NORMALIZED = "normalized", "Normalized"
    ENRICHED = "enriched", "Enriched"
    MANUAL_REVIEW = "manual_review", "Manual Review"
