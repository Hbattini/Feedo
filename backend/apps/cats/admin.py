from django.contrib import admin

from apps.cats.models import Cat, CatCondition, CatEvent, CatMeasurement


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at", "updated_at")
    list_display = ("name", "owner", "born_at", "created_at")
    search_fields = ("name", "owner__email")


@admin.register(CatMeasurement)
class CatMeasurementAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at")
    list_display = ("cat", "weight_value", "weight_unit", "measured_at", "source")


@admin.register(CatCondition)
class CatConditionAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "public_id", "created_at", "updated_at")
    list_display = ("cat", "condition_code", "source", "resolved_at")


@admin.register(CatEvent)
class CatEventAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "public_id",
        "event_id",
        "cat",
        "food",
        "recommendation_item",
        "event_type",
        "occurred_at",
        "source",
        "metadata",
        "created_at",
    )
    list_display = ("cat", "event_type", "food", "occurred_at", "event_id")
    list_filter = ("event_type", "source")
    search_fields = ("cat__name",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
