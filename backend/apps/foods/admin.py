from django.contrib import admin

from apps.foods.models import Food, FoodAttribute, FoodNutritionalTag, FoodRawSource


@admin.register(FoodRawSource)
class FoodRawSourceAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "payload", "payload_hash", "fetched_at")
    list_display = ("source", "external_id", "validation_status", "fetched_at")
    list_filter = ("source", "validation_status")
    search_fields = ("external_id",)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at", "updated_at")
    list_display = ("brand_name", "canonical_name", "catalog_status")
    list_filter = ("catalog_status",)
    search_fields = ("brand_name", "canonical_name")


@admin.register(FoodAttribute)
class FoodAttributeAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at", "updated_at", "feature_json")
    list_display = ("food", "life_stage", "texture", "primary_protein", "is_wet")


@admin.register(FoodNutritionalTag)
class FoodNutritionalTagAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at")
    list_display = ("food", "nutritional_tag", "source", "confidence")
