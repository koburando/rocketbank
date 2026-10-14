"""
Django admin configuration for the Transactions app.
"""

from django.contrib import admin

from apps.transactions.models import Transaction, TransactionCategory


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    """Admin for TransactionCategory."""

    list_display = ("name", "slug", "icon", "is_expense")
    list_filter = ("is_expense",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin for Transaction records."""

    list_display = (
        "reference_number",
        "transaction_type",
        "amount",
        "currency",
        "status",
        "sender_account",
        "receiver_account",
        "created_at",
    )
    list_filter = (
        "status",
        "transaction_type",
        "currency",
        "created_at",
    )
    search_fields = (
        "reference_number",
        "description",
        "sender_account__iban",
        "receiver_account__iban",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "reference_number",
        "created_at",
        "updated_at",
    )
    autocomplete_fields = (
        "sender_account",
        "receiver_account",
        "currency",
        "category",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "reference_number",
                    "transaction_type",
                )
            },
        ),
        (
            "Accounts",
            {
                "fields": (
                    "sender_account",
                    "receiver_account",
                )
            },
        ),
        (
            "Amount",
            {"fields": ("amount", "currency", "category")},
        ),
        (
            "Status & Details",
            {"fields": ("status", "description")},
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
