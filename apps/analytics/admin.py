"""
Django admin configuration for the Analytics app.
"""

from django.contrib import admin

from apps.analytics.models import SavingGoal


@admin.register(SavingGoal)
class SavingGoalAdmin(admin.ModelAdmin):
    """Admin for SavingGoal tracking."""

    list_display = (
        "title",
        "user",
        "target_amount",
        "current_amount",
        "display_progress",
        "deadline",
        "is_achieved",
    )
    list_filter = ("is_achieved", "category")
    search_fields = ("title", "user__email", "category")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user",)

    @admin.display(description="Progress")
    def display_progress(self, obj):
        return f"{obj.progress_percent:.1f}%"
