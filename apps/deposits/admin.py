"""
Django admin configuration for the Deposits app.
"""

from django.contrib import admin

from apps.deposits.models import DepositProduct, UserDeposit


@admin.register(DepositProduct)
class DepositProductAdmin(admin.ModelAdmin):
    """Admin for DepositProduct catalog."""

    list_display = (
        "title",
        "slug",
        "interest_rate",
        "min_amount",
        "term_months",
        "is_early_withdrawal_allowed",
        "is_active",
    )
    list_filter = (
        "is_active",
        "is_early_withdrawal_allowed",
    )
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("interest_rate", "is_active")
    readonly_fields = ("created_at", "updated_at")


@admin.register(UserDeposit)
class UserDepositAdmin(admin.ModelAdmin):
    """Admin for user deposits."""

    list_display = (
        "user",
        "product",
        "amount",
        "accrued_interest",
        "status",
        "start_date",
        "end_date",
    )
    list_filter = ("status", "product")
    search_fields = (
        "user__email",
        "product__title",
        "account__iban",
    )
    date_hierarchy = "start_date"
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user", "account", "product")
