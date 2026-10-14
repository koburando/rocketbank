"""
Django admin configuration for the Support app.
"""

from django.contrib import admin

from apps.support.models import FAQ, SupportTicket, TicketReview


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin for FAQ management."""

    list_display = (
        "question",
        "category",
        "order",
        "is_published",
        "created_at",
    )
    list_filter = ("is_published", "category")
    search_fields = ("question", "answer", "category")
    list_editable = ("order", "is_published")
    readonly_fields = ("created_at", "updated_at")


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    """Admin for support tickets."""

    list_display = (
        "pk",
        "subject",
        "user",
        "status",
        "priority",
        "assigned_to",
        "created_at",
    )
    list_filter = ("status", "priority", "created_at")
    search_fields = (
        "subject",
        "description",
        "user__email",
    )
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user", "assigned_to")


@admin.register(TicketReview)
class TicketReviewAdmin(admin.ModelAdmin):
    """Admin for ticket reviews/ratings."""

    list_display = (
        "user",
        "ticket",
        "rating",
        "is_helpful_count",
        "created_at",
    )
    list_filter = ("rating", "created_at")
    search_fields = ("user__email", "comment")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user", "ticket")
