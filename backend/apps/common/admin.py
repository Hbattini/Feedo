from django.contrib import admin

from apps.common.models import ConditionCode, EventType, LifeStage, NutritionalTag, Protein, Texture


@admin.register(Protein, Texture, LifeStage, NutritionalTag, ConditionCode, EventType)
class TaxonomyAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at", "updated_at")
    list_display = ("code", "label", "is_active")
    search_fields = ("code", "label")
    list_filter = ("is_active",)
