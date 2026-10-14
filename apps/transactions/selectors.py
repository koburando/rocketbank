"""
Query selectors / read-only data access layer for the Transactions app.

Provides optimized queries for transaction history, monthly analytics,
and spending breakdowns using Django ORM aggregation.
"""

from decimal import Decimal

from django.db.models import (
    Count,
    F,
    OuterRef,
    Q,
    Subquery,
    Sum,
)
from django.db.models.functions import TruncMonth

from apps.transactions.models import Transaction


def get_account_transactions(account, limit=50):
    """
    Get recent transactions for an account (sent or received).

    Uses select_related for efficient joins.
    """
    return (
        Transaction.objects.filter(
            Q(sender_account=account)
            | Q(receiver_account=account)
        )
        .select_related(
            "sender_account__owner",
            "receiver_account__owner",
            "currency",
            "category",
        )
        .order_by("-created_at")[:limit]
    )


def get_monthly_analytics(account):
    """
    Monthly transaction analytics for an account.

    Returns aggregated spend/income per month using TruncMonth.
    """
    outgoing = (
        Transaction.objects.filter(
            sender_account=account,
            status=Transaction.TransactionStatus.COMPLETED,
        )
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(
            total_spent=Sum("amount"),
            txn_count=Count("id"),
        )
        .order_by("-month")
    )

    incoming = (
        Transaction.objects.filter(
            receiver_account=account,
            status=Transaction.TransactionStatus.COMPLETED,
        )
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(
            total_received=Sum("amount"),
            txn_count=Count("id"),
        )
        .order_by("-month")
    )

    return {
        "outgoing_by_month": list(outgoing),
        "incoming_by_month": list(incoming),
    }


def get_spending_by_category(account):
    """
    Get spending breakdown by category for an account.

    Uses F expressions and aggregation.
    """
    return (
        Transaction.objects.filter(
            sender_account=account,
            status=Transaction.TransactionStatus.COMPLETED,
            category__isnull=False,
        )
        .values(
            category_name=F("category__name"),
            category_slug=F("category__slug"),
        )
        .annotate(
            total_amount=Sum("amount"),
            txn_count=Count("id"),
        )
        .order_by("-total_amount")
    )


def get_user_transaction_summary(user):
    """
    Aggregate transaction summary for a user across all accounts.

    Uses Subquery and OuterRef for correlated lookups.
    """
    from apps.accounts.models import BankAccount

    user_accounts = BankAccount.all_objects.filter(
        owner=user, is_deleted=False
    )

    total_sent_subquery = Subquery(
        Transaction.objects.filter(
            sender_account=OuterRef("pk"),
            status=Transaction.TransactionStatus.COMPLETED,
        )
        .values("sender_account")
        .annotate(total=Sum("amount"))
        .values("total")[:1]
    )

    total_received_subquery = Subquery(
        Transaction.objects.filter(
            receiver_account=OuterRef("pk"),
            status=Transaction.TransactionStatus.COMPLETED,
        )
        .values("receiver_account")
        .annotate(total=Sum("amount"))
        .values("total")[:1]
    )

    return user_accounts.annotate(
        total_sent=total_sent_subquery,
        total_received=total_received_subquery,
    ).values(
        "iban",
        "account_type",
        "balance",
        "total_sent",
        "total_received",
    )


def get_recent_completed_transactions(limit: int = 20):
    """Get globally recent completed transactions."""
    return (
        Transaction.objects.completed()
        .select_related(
            "sender_account__owner",
            "receiver_account__owner",
            "currency",
        )
        .order_by("-created_at")[:limit]
    )


def get_transaction_volume_by_month():
    """Get total transaction volume and count by month."""
    return (
        Transaction.objects.filter(
            status=Transaction.TransactionStatus.COMPLETED,
        )
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(
            total_volume=Sum("amount"),
            total_count=Count("id"),
            avg_amount=Sum("amount") / Count("id"),
        )
        .order_by("-month")
    )


def get_top_senders(limit: int = 10):
    """Get top senders by total amount sent."""
    return (
        Transaction.objects.filter(
            status=Transaction.TransactionStatus.COMPLETED,
            sender_account__isnull=False,
        )
        .values(
            sender_email=F("sender_account__owner__email"),
            sender_iban=F("sender_account__iban"),
        )
        .annotate(
            total_sent=Sum("amount"),
            txn_count=Count("id"),
        )
        .order_by("-total_sent")[:limit]
    )
