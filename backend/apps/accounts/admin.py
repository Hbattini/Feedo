from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User


@admin.register(User)
class FeedoUserAdmin(UserAdmin):
    readonly_fields = ("id", "public_id", "date_joined", "last_login")
    list_display = ("email", "username", "is_active", "is_staff", "date_joined")
    search_fields = ("email", "username")
