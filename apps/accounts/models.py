"""
Domain models for the Accounts app.

Provides Currency, BankAccount (with soft-delete), Beneficiary,
and SavedBeneficiary models for managing banking accounts.
"""

import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from apps.core.models import SoftDeleteManager, SoftDeleteModel, TimeStampedModel
from apps.core.validators import validate_iban


# ──────────────────────────────────────────────
# Custom Managers
# ──────────────────────────────────────────────


class BankAccountQuerySet(models.QuerySet):
    """Custom QuerySet for BankAccount with business-logic filters."""

    def active(self):
        return self.filter(
            status=BankAccount.AccountStatus.ACTIVE,
            is_deleted=False,
        )

    def frozen(self):
        return self.filter(status=BankAccount.AccountStatus.FROZEN)

    def by_owner(self, user):
        return self.filter(owner=user, is_deleted=False)


class BankAccountManager(SoftDeleteManager):
    """Manager for BankAccount that excludes soft-deleted records."""

    def get_queryset(self):
        return BankAccountQuerySet(self.model, using=self._db).active()

    def active(self):
        return self.get_queryset()

    def all_active(self):
        """Return all non-deleted accounts regardless of status."""
        return BankAccountQuerySet(
            self.model, using=self._db
        ).filter(is_deleted=False)


# ──────────────────────────────────────────────
# Models
# ──────────────────────────────────────────────


class Currency(TimeStampedModel):
    """Supported currencies with exchange rates to KZT."""

    code = models.CharField(
        "currency code",
        max_length=3,
        unique=True,
        help_text="ISO 4217 code (e.g. KZT, USD, EUR)",
    )
    name = models.CharField("currency name", max_length=50)
    symbol = models.CharField("symbol", max_length=5)
    exchange_rate_to_kzt = models.DecimalField(
        "exchange rate to KZT",
        max_digits=12,
        decimal_places=4,
        default=1,
    )
    is_active = models.BooleanField("active", default=True)

    class Meta:
        verbose_name = "currency"
        verbose_name_plural = "currencies"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} — {self.name}"

    def get_absolute_url(self):
        return reverse(
            "admin:accounts_currency_change", args=[self.pk]
        )


class BankAccount(SoftDeleteModel):
    """
    Bank account with UUID primary key, IBAN, and soft-delete.

    Supports CHECKING, SAVINGS, BUSINESS, and DEPOSIT account types.
    """

    class AccountType(models.TextChoices):
        CHECKING = "CHECKING", "Checking"
        SAVINGS = "SAVINGS", "Savings"
        BUSINESS = "BUSINESS", "Business"
        DEPOSIT = "DEPOSIT", "Deposit"

    class AccountStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        FROZEN = "FROZEN", "Frozen"
        CLOSED = "CLOSED", "Closed"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="bank_accounts",
        verbose_name="owner",
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="accounts",
        verbose_name="currency",
    )
    iban = models.CharField(
        "IBAN",
        max_length=34,
        unique=True,
        validators=[validate_iban],
    )
    account_type = models.CharField(
        "account type",
        max_length=10,
        choices=AccountType.choices,
        default=AccountType.CHECKING,
    )
    balance = models.DecimalField(
        "balance",
        max_digits=15,
        decimal_places=2,
        default=0,
    )
    status = models.CharField(
        "status",
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )
    opened_at = models.DateTimeField("opened at", auto_now_add=True)

    objects = BankAccountManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "bank account"
        verbose_name_plural = "bank accounts"
        ordering = ["-opened_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte=0),
                name="accounts_balance_non_negative",
            ),
            models.UniqueConstraint(
                fields=["owner", "currency", "account_type"],
                name="unique_account_per_type_currency",
            ),
        ]
        indexes = [
            models.Index(
                fields=["iban"], name="idx_account_iban"
            ),
            models.Index(
                fields=["status"], name="idx_account_status"
            ),
            models.Index(
                fields=["owner"], name="idx_account_owner"
            ),
        ]

    def __str__(self):
        return f"{self.iban} ({self.get_account_type_display()})"

    def get_absolute_url(self):
        return reverse(
            "admin:accounts_bankaccount_change", args=[self.pk]
        )

    def clean(self):
        super().clean()
        if self.iban:
            validate_iban(self.iban)


class Beneficiary(TimeStampedModel):
    """A saved recipient account for quick transfers."""

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="beneficiaries",
        verbose_name="owner",
    )
    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name="beneficiary_entries",
        verbose_name="recipient account",
    )

    class Meta:
        verbose_name = "beneficiary"
        verbose_name_plural = "beneficiaries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner.email} → {self.account.iban}"

    def get_absolute_url(self):
        return reverse(
            "admin:accounts_beneficiary_change", args=[self.pk]
        )


class SavedBeneficiary(TimeStampedModel):
    """Through model for beneficiary with nickname and favorite flag."""

    beneficiary = models.ForeignKey(
        Beneficiary,
        on_delete=models.CASCADE,
        related_name="saved_entries",
        verbose_name="beneficiary",
    )
    nickname = models.CharField("nickname", max_length=100)
    is_favorite = models.BooleanField("favorite", default=False)

    class Meta:
        verbose_name = "saved beneficiary"
        verbose_name_plural = "saved beneficiaries"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["beneficiary", "nickname"],
                name="unique_beneficiary_nickname",
            ),
        ]

    def __str__(self):
        return f"{self.nickname} ({self.beneficiary})"

    def get_absolute_url(self):
        return reverse(
            "admin:accounts_savedbeneficiary_change",
            args=[self.pk],
        )
