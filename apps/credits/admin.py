"""
Django admin configuration for the Credits app.
"""

from django.contrib import admin
from django.utils import timezone

from apps.credits.models import LoanApplication, LoanProduct, LoanSchedule


# ──────────────────────────────────────────────
# Admin Actions
# ──────────────────────────────────────────────


@admin.action(description="Approve selected loan applications")
def approve_loan_applications(modeladmin, request, queryset):
    """Approve selected loan applications."""
    from apps.credits.services import approve_loan

    approved = 0
    for loan in queryset.filter(
        status__in=[
            LoanApplication.LoanStatus.SUBMITTED,
            LoanApplication.LoanStatus.UNDER_REVIEW,
        ]
    ):
        approve_loan(loan)
        approved += 1

    modeladmin.message_user(
        request, f"{approved} loan(s) approved."
    )


# ──────────────────────────────────────────────
# Inlines
# ──────────────────────────────────────────────


class LoanScheduleInline(admin.TabularInline):
    """Inline amortization schedule within loan admin."""

    model = LoanSchedule
    extra = 0
    readonly_fields = (
        "installment_number",
        "due_date",
        "principal_amount",
        "interest_amount",
        "is_paid",
        "paid_at",
    )
    fields = (
        "installment_number",
        "due_date",
        "principal_amount",
        "interest_amount",
        "is_paid",
        "paid_at",
    )
    can_delete = False


# ──────────────────────────────────────────────
# Model Admins
# ──────────────────────────────────────────────


@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    """Admin for LoanProduct catalog."""

    list_display = (
        "title",
        "slug",
        "interest_rate",
        "min_amount",
        "max_amount",
        "min_term_months",
        "max_term_months",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("interest_rate", "is_active")
    readonly_fields = ("created_at", "updated_at")


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    """Admin for LoanApplication with schedule inline."""

    inlines = [LoanScheduleInline]
    actions = [approve_loan_applications]

    list_display = (
        "pk",
        "user",
        "product",
        "requested_amount",
        "term_months",
        "status",
        "display_approved",
        "created_at",
    )
    list_filter = ("status", "product", "created_at")
    search_fields = (
        "user__email",
        "user__username",
        "product__title",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "approved_at",
        "created_at",
        "updated_at",
    )
    autocomplete_fields = ("user", "product")

    fieldsets = (
        (
            None,
            {"fields": ("user", "product")},
        ),
        (
            "Loan Details",
            {
                "fields": (
                    "requested_amount",
                    "term_months",
                    "monthly_income",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "approved_at",
                    "rejection_reason",
                )
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    @admin.display(
        boolean=True,
        description="Approved",
        ordering="approved_at",
    )
    def display_approved(self, obj):
        return obj.approved_at is not None


@admin.register(LoanSchedule)
class LoanScheduleAdmin(admin.ModelAdmin):
    """Admin for individual schedule entries."""

    list_display = (
        "loan",
        "installment_number",
        "due_date",
        "principal_amount",
        "interest_amount",
        "is_paid",
    )
    list_filter = ("is_paid", "due_date")
    search_fields = ("loan__user__email",)
    readonly_fields = ("created_at", "updated_at")
