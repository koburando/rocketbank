"""
Query selectors / read-only data access layer for the Accounts app.

Provides optimized queries for account summaries, balance aggregation,
and user portfolio views using Django ORM aggregation.
"""

from decimal import Decimal

from django.db.models import Case, Count, DecimalField, Q, Sum, When

from apps.accounts.models import BankAccount


def get_user_accounts(user):
    """
    Get all active accounts for a user with related currency.

    Uses select_related to minimize DB queries.
    """
    return (
        BankAccount.all_objects.filter(
            owner=user, is_deleted=False
        )
        .select_related("currency")
        .order_by("-opened_at")
    )


def get_balance_summary(user) -> dict:
    """
    Get aggregated balance summary for a user's accounts.

    Returns dict with total_balance, account_count,
    and per-type breakdown.
    """
    accounts = BankAccount.all_objects.filter(
        owner=user,
        is_deleted=False,
        status=BankAccount.AccountStatus.ACTIVE,
    )

    summary = accounts.aggregate(
        total_balance=Sum("balance"),
        account_count=Count("id"),
        checking_balance=Sum(
            Case(
                When(
                    account_type=BankAccount.AccountType.CHECKING,
                    then="balance",
                ),
                default=Decimal("0"),
                output_field=DecimalField(),
            )
        ),
        savings_balance=Sum(
            Case(
                When(
                    account_type=BankAccount.AccountType.SAVINGS,
                    then="balance",
                ),
                default=Decimal("0"),
                output_field=DecimalField(),
            )
        ),
        business_balance=Sum(
            Case(
                When(
                    account_type=BankAccount.AccountType.BUSINESS,
                    then="balance",
                ),
                default=Decimal("0"),
                output_field=DecimalField(),
            )
        ),
    )

    return {
        "total_balance": summary["total_balance"] or Decimal("0"),
        "account_count": summary["account_count"] or 0,
        "checking_balance": summary["checking_balance"]
        or Decimal("0"),
        "savings_balance": summary["savings_balance"]
        or Decimal("0"),
        "business_balance": summary["business_balance"]
        or Decimal("0"),
    }


def get_accounts_with_cards(user):
    """
    Get user accounts with prefetched cards and card products.

    Uses prefetch_related for efficient related object loading.
    """
    return (
        BankAccount.all_objects.filter(
            owner=user, is_deleted=False
        )
        .select_related("currency")
        .prefetch_related("cards__product")
        .order_by("-opened_at")
    )


def get_high_value_accounts(min_balance: Decimal = Decimal("1000000")):
    """Get all active accounts above a minimum balance threshold."""
    return (
        BankAccount.all_objects.filter(
            is_deleted=False,
            status=BankAccount.AccountStatus.ACTIVE,
            balance__gte=min_balance,
        )
        .select_related("owner", "currency")
        .order_by("-balance")
    )


def get_account_type_distribution():
    """Get count of accounts grouped by type and status."""
    return (
        BankAccount.all_objects.filter(is_deleted=False)
        .values("account_type", "status")
        .annotate(count=Count("id"))
        .order_by("account_type", "status")
    )


def get_frozen_accounts():
    """Get all currently frozen accounts with owner info."""
    return (
        BankAccount.all_objects.filter(
            status=BankAccount.AccountStatus.FROZEN,
            is_deleted=False,
        )
        .select_related("owner", "currency")
        .order_by("-updated_at")
    )


def search_account_by_iban(iban: str):
    """Look up an account by its IBAN, including soft-deleted."""
    return (
        BankAccount.all_objects.filter(
            iban=iban
        )
        .select_related("owner", "currency")
        .first()
    )


def get_currency_balance_summary():
    """Get total balance across all active accounts per currency."""
    return (
        BankAccount.all_objects.filter(
            is_deleted=False,
            status=BankAccount.AccountStatus.ACTIVE,
        )
        .values("currency__code", "currency__name")
        .annotate(
            total_balance=Sum("balance"),
            account_count=Count("id"),
        )
        .order_by("currency__code")
    )
