"""
Django admin configuration for the Accounts app.

Includes HighValueAccountFilter, CSV export action,
freeze accounts action, and BankCard inline.
"""

import csv

from django.contrib import admin
from django.http import HttpResponse

from apps.accounts.models import (
    BankAccount,
    Beneficiary,
    Currency,
    SavedBeneficiary,
)
from apps.cards.models import BankCard

# ──────────────────────────────────────────────
# Custom Filters
# ──────────────────────────────────────────────


class HighValueAccountFilter(admin.SimpleListFilter):
    """Filter accounts by high-value balance threshold."""

    title = "balance tier"
    parameter_name = "balance_tier"

    def lookups(self, request, model_admin):
        return [
            ("high", "High Value (≥1,000,000)"),
            ("medium", "Medium (100,000–999,999)"),
            ("low", "Low (<100,000)"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "high":
            return queryset.filter(balance__gte=1_000_000)
        if self.value() == "medium":
            return queryset.filter(balance__gte=100_000, balance__lt=1_000_000)
        if self.value() == "low":
            return queryset.filter(balance__lt=100_000)
        return queryset


# ──────────────────────────────────────────────
# Admin Actions
# ──────────────────────────────────────────────


@admin.action(description="Export selected records to CSV")
def export_to_csv(modeladmin, request, queryset):
    """Export selected records to a CSV file."""
    meta = modeladmin.model._meta
    field_names = [f.name for f in meta.fields]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{meta.verbose_name_plural}.csv"'

    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in field_names])
    return response


@admin.action(description="Freeze selected accounts")
def freeze_accounts(modeladmin, request, queryset):
    """Freeze selected bank accounts."""
    updated = queryset.update(status=BankAccount.AccountStatus.FROZEN)
    modeladmin.message_user(request, f"{updated} account(s) frozen.")


# ──────────────────────────────────────────────
# Inlines
# ──────────────────────────────────────────────


class BankCardInline(admin.TabularInline):
    """Inline display of cards within BankAccount admin."""

    model = BankCard
    extra = 0
    readonly_fields = (
        "card_number_masked",
        "status",
        "issued_at",
    )
    fields = (
        "product",
        "card_number_masked",
        "expiry_date",
        "status",
        "daily_limit",
    )


class SavedBeneficiaryInline(admin.TabularInline):
    """Inline saved beneficiary entries."""

    model = SavedBeneficiary
    extra = 0


# ──────────────────────────────────────────────
# Model Admins
# ──────────────────────────────────────────────


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """Admin for Currency model."""

    list_display = (
        "code",
        "name",
        "symbol",
        "exchange_rate_to_kzt",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("code", "name")
    list_editable = ("exchange_rate_to_kzt", "is_active")


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    """Admin for BankAccount with cards inline and custom actions."""

    inlines = [BankCardInline]
    actions = [export_to_csv, freeze_accounts]

    list_display = (
        "iban",
        "owner",
        "account_type",
        "currency",
        "balance",
        "status",
        "display_is_deleted",
        "opened_at",
    )
    list_filter = (
        "account_type",
        "status",
        "currency",
        HighValueAccountFilter,
        "is_deleted",
    )
    search_fields = ("iban", "owner__email", "owner__username")
    date_hierarchy = "opened_at"
    readonly_fields = (
        "id",
        "iban",
        "opened_at",
        "created_at",
        "updated_at",
    )
    autocomplete_fields = ("owner", "currency")

    fieldsets = (
        (
            None,
            {"fields": ("id", "owner", "currency", "iban")},
        ),
        (
            "Account Details",
            {
                "fields": (
                    "account_type",
                    "balance",
                    "status",
                )
            },
        ),
        (
            "Soft Delete",
            {
                "classes": ("collapse",),
                "fields": ("is_deleted", "deleted_at"),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("opened_at", "created_at", "updated_at"),
            },
        ),
    )

    def get_queryset(self, request):
        """Show all accounts including soft-deleted."""
        return BankAccount.all_objects.select_related("owner", "currency")

    @admin.display(boolean=True, description="Deleted", ordering="is_deleted")
    def display_is_deleted(self, obj):
        return obj.is_deleted


@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    """Admin for Beneficiary model."""

    inlines = [SavedBeneficiaryInline]
    list_display = ("owner", "account", "created_at")
    search_fields = (
        "owner__email",
        "account__iban",
    )
    autocomplete_fields = ("owner", "account")


@admin.register(SavedBeneficiary)
class SavedBeneficiaryAdmin(admin.ModelAdmin):
    """Admin for SavedBeneficiary."""

    list_display = (
        "nickname",
        "beneficiary",
        "is_favorite",
        "created_at",
    )
    list_filter = ("is_favorite",)
    search_fields = ("nickname",)
