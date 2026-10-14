"""
Query selectors / read-only data access layer for the Credits app.
"""

from django.db.models import Count, Sum

from apps.credits.models import LoanApplication, LoanSchedule


def get_user_loans(user):
    """Get all loan applications for a user with product info."""
    return (
        LoanApplication.objects.filter(user=user)
        .select_related("product")
        .prefetch_related("schedule_entries")
        .order_by("-created_at")
    )


def get_active_loans(user):
    """Get active (disbursed) loans for a user."""
    return (
        LoanApplication.objects.filter(
            user=user,
            status__in=[
                LoanApplication.LoanStatus.APPROVED,
                LoanApplication.LoanStatus.DISBURSED,
            ],
        )
        .select_related("product")
        .order_by("-created_at")
    )


def get_loan_schedule(loan_application):
    """Get full schedule for a loan application."""
    return (
        LoanSchedule.objects.filter(loan=loan_application)
        .order_by("installment_number")
    )


def get_overdue_installments(user):
    """Get unpaid installments past their due date."""
    from django.utils import timezone

    return (
        LoanSchedule.objects.filter(
            loan__user=user,
            is_paid=False,
            due_date__lt=timezone.now().date(),
        )
        .select_related("loan__product")
        .order_by("due_date")
    )


def get_loan_portfolio_summary():
    """Get aggregate summary of all loans in the system."""
    return LoanApplication.objects.aggregate(
        total_applications=Count("id"),
        total_approved=Count(
            "id",
            filter=models_Q(
                status=LoanApplication.LoanStatus.APPROVED,
            ),
        ),
        total_disbursed_amount=Sum(
            "requested_amount",
            filter=models_Q(
                status=LoanApplication.LoanStatus.DISBURSED,
            ),
        ),
    )


def models_Q(**kwargs):
    """Helper to create Q objects for aggregation filters."""
    from django.db.models import Q

    return Q(**kwargs)
