"""
Django admin configuration for the Notifications app.
"""

from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin for user notifications."""

    list_display = (
        "title",
        "user",
        "notification_type",
        "is_read",
        "created_at",
    )
    list_filter = ("notification_type", "is_read", "created_at")
    search_fields = ("title", "message", "user__email")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "read_at")
    autocomplete_fields = ("user",)
