"""
Django admin configuration for the Cards app.
"""

from django.contrib import admin

from apps.cards.models import BankCard, CardProduct


@admin.register(CardProduct)
class CardProductAdmin(admin.ModelAdmin):
    """Admin for CardProduct catalog."""

    list_display = (
        "title",
        "slug",
        "tier",
        "cashback_percent",
        "annual_fee",
        "is_active",
        "display_card_count",
    )
    list_filter = ("tier", "is_active")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("cashback_percent", "annual_fee", "is_active")
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Cards Issued")
    def display_card_count(self, obj):
        return obj.issued_cards.count()


@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    """Admin for BankCard instances."""

    list_display = (
        "card_number_masked",
        "account",
        "product",
        "status",
        "expiry_date",
        "daily_limit",
        "issued_at",
    )
    list_filter = ("status", "product__tier")
    search_fields = (
        "card_number_masked",
        "account__iban",
        "account__owner__email",
    )
    date_hierarchy = "issued_at"
    readonly_fields = (
        "issued_at",
        "created_at",
        "updated_at",
    )
    autocomplete_fields = ("account", "product")
