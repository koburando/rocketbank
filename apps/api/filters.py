"""
Django-filter FilterSets for RocketBank REST API endpoints.
Provides filtering for accounts, cards, products, transactions, loans, deposits, and reviews.
"""

import django_filters

from apps.accounts.models import BankAccount
from apps.analytics.models import SavingGoal
from apps.cards.models import BankCard, CardProduct
from apps.credits.models import LoanApplication, LoanProduct
from apps.deposits.models import DepositProduct, UserDeposit
from apps.support.models import ProductReview
from apps.transactions.models import Transaction


class BankAccountFilter(django_filters.FilterSet):
    """Filter for BankAccount queryset."""

    min_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="gte")
    max_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="lte")
    currency = django_filters.CharFilter(field_name="currency__code", lookup_expr="iexact")
    account_type = django_filters.ChoiceFilter(choices=BankAccount.AccountType.choices)
    status = django_filters.ChoiceFilter(choices=BankAccount.AccountStatus.choices)

    class Meta:
        model = BankAccount
        fields = ["account_type", "status", "currency", "min_balance", "max_balance"]


class CardProductFilter(django_filters.FilterSet):
    """Filter for CardProduct catalog."""

    tier = django_filters.ChoiceFilter(choices=CardProduct.CardTier.choices)
    min_cashback = django_filters.NumberFilter(field_name="cashback_percent", lookup_expr="gte")
    max_cashback = django_filters.NumberFilter(field_name="cashback_percent", lookup_expr="lte")
    max_annual_fee = django_filters.NumberFilter(field_name="annual_fee", lookup_expr="lte")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = CardProduct
        fields = ["tier", "is_active", "min_cashback", "max_cashback", "max_annual_fee"]


class BankCardFilter(django_filters.FilterSet):
    """Filter for issued BankCards."""

    status = django_filters.ChoiceFilter(choices=BankCard.CardStatus.choices)
    tier = django_filters.CharFilter(field_name="product__tier", lookup_expr="iexact")
    product_slug = django_filters.CharFilter(field_name="product__slug", lookup_expr="iexact")

    class Meta:
        model = BankCard
        fields = ["status", "tier", "product_slug"]


class TransactionFilter(django_filters.FilterSet):
    """Filter for financial transactions."""

    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="iexact")
    currency = django_filters.CharFilter(field_name="currency__code", lookup_expr="iexact")
    status = django_filters.ChoiceFilter(choices=Transaction.TransactionStatus.choices)
    transaction_type = django_filters.ChoiceFilter(choices=Transaction.TransactionType.choices)
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = [
            "status",
            "transaction_type",
            "category",
            "currency",
            "min_amount",
            "max_amount",
            "created_after",
            "created_before",
        ]


class LoanProductFilter(django_filters.FilterSet):
    """Filter for LoanProduct catalog."""

    max_interest_rate = django_filters.NumberFilter(field_name="interest_rate", lookup_expr="lte")
    min_amount = django_filters.NumberFilter(field_name="min_amount", lookup_expr="lte")
    max_amount = django_filters.NumberFilter(field_name="max_amount", lookup_expr="gte")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = LoanProduct
        fields = ["is_active", "max_interest_rate", "min_amount", "max_amount"]


class LoanApplicationFilter(django_filters.FilterSet):
    """Filter for LoanApplications."""

    status = django_filters.ChoiceFilter(choices=LoanApplication.LoanStatus.choices)
    product_slug = django_filters.CharFilter(field_name="product__slug", lookup_expr="iexact")

    class Meta:
        model = LoanApplication
        fields = ["status", "product_slug"]


class DepositProductFilter(django_filters.FilterSet):
    """Filter for DepositProduct catalog."""

    min_interest_rate = django_filters.NumberFilter(field_name="interest_rate", lookup_expr="gte")
    term_months = django_filters.NumberFilter(field_name="term_months")
    is_early_withdrawal_allowed = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = DepositProduct
        fields = ["is_active", "term_months", "min_interest_rate", "is_early_withdrawal_allowed"]


class UserDepositFilter(django_filters.FilterSet):
    """Filter for customer fixed deposits."""

    status = django_filters.ChoiceFilter(choices=UserDeposit.DepositStatus.choices)
    product_slug = django_filters.CharFilter(field_name="product__slug", lookup_expr="iexact")

    class Meta:
        model = UserDeposit
        fields = ["status", "product_slug"]


class SavingGoalFilter(django_filters.FilterSet):
    """Filter for user saving goals."""

    category = django_filters.CharFilter(lookup_expr="iexact")
    is_achieved = django_filters.BooleanFilter()

    class Meta:
        model = SavingGoal
        fields = ["category", "is_achieved"]


class ProductReviewFilter(django_filters.FilterSet):
    """Filter for product reviews."""

    product_type = django_filters.CharFilter(lookup_expr="iexact")
    product_id = django_filters.CharFilter(lookup_expr="iexact")
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")

    class Meta:
        model = ProductReview
        fields = ["product_type", "product_id", "min_rating"]
