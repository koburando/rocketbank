from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for the custom User model."""

    list_display = ("email", "username", "phone_number", "is_verified", "is_staff")
    list_filter = ("is_verified", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "username", "phone_number")
    ordering = ("-date_joined",)
