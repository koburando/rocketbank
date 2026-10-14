"""
Domain models for the Transactions app.

Provides TransactionCategory and Transaction with UUID primary key,
state-machine transitions, and custom manager.
"""

import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel

# ──────────────────────────────────────────────
# Custom Managers
# ──────────────────────────────────────────────


class TransactionQuerySet(models.QuerySet):
    """QuerySet with business-logic filters for transactions."""

    def completed(self):
        return self.filter(status=Transaction.TransactionStatus.COMPLETED)

    def pending(self):
        return self.filter(status=Transaction.TransactionStatus.PENDING)

    def by_account(self, account):
        return self.filter(models.Q(sender_account=account) | models.Q(receiver_account=account))

    def expenses(self):
        return self.filter(sender_account__isnull=False)

    def income(self):
        return self.filter(receiver_account__isnull=False)


class TransactionManager(models.Manager):
    """Custom manager for Transaction."""

    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)

    def completed(self):
        return self.get_queryset().completed()

    def pending(self):
        return self.get_queryset().pending()


# ──────────────────────────────────────────────
# Models
# ──────────────────────────────────────────────


class TransactionCategory(TimeStampedModel):
    """Category for organizing transactions (e.g. Food, Transport)."""

    name = models.CharField("name", max_length=100)
    slug = models.SlugField("slug", unique=True)
    icon = models.CharField(
        "icon class",
        max_length=50,
        blank=True,
        help_text="CSS icon class name",
    )
    is_expense = models.BooleanField("is expense", default=True)

    class Meta:
        verbose_name = "transaction category"
        verbose_name_plural = "transaction categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "admin:transactions_transactioncategory_change",
            args=[self.pk],
        )


class Transaction(TimeStampedModel):
    """
    Financial transaction between accounts.

    Supports transfers, deposits, withdrawals, payments, and fees.
    Includes state-machine transition validation.
    """

    class TransactionStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"
        REVERSED = "REVERSED", "Reversed"

    class TransactionType(models.TextChoices):
        TRANSFER = "TRANSFER", "Transfer"
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAWAL = "WITHDRAWAL", "Withdrawal"
        PAYMENT = "PAYMENT", "Payment"
        FEE = "FEE", "Fee"

    ALLOWED_TRANSITIONS = {
        TransactionStatus.PENDING: [
            TransactionStatus.COMPLETED,
            TransactionStatus.FAILED,
            TransactionStatus.CANCELLED,
        ],
        TransactionStatus.COMPLETED: [TransactionStatus.REVERSED],
        TransactionStatus.FAILED: [],
        TransactionStatus.CANCELLED: [],
        TransactionStatus.REVERSED: [],
    }

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    sender_account = models.ForeignKey(
        "accounts.BankAccount",
        on_delete=models.PROTECT,
        related_name="outgoing_transactions",
        verbose_name="sender account",
        null=True,
        blank=True,
    )
    receiver_account = models.ForeignKey(
        "accounts.BankAccount",
        on_delete=models.PROTECT,
        related_name="incoming_transactions",
        verbose_name="receiver account",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
        verbose_name="category",
    )
    amount = models.DecimalField(
        "amount",
        max_digits=15,
        decimal_places=2,
    )
    currency = models.ForeignKey(
        "accounts.Currency",
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="currency",
    )
    status = models.CharField(
        "status",
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    transaction_type = models.CharField(
        "type",
        max_length=12,
        choices=TransactionType.choices,
        default=TransactionType.TRANSFER,
    )
    description = models.TextField("description", blank=True)
    reference_number = models.CharField(
        "reference number",
        max_length=50,
        unique=True,
        db_index=True,
    )

    objects = TransactionManager()

    class Meta:
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="transactions_amount_positive",
            ),
        ]
        indexes = [
            models.Index(
                fields=["reference_number"],
                name="idx_txn_reference",
            ),
            models.Index(fields=["status"], name="idx_txn_status"),
            models.Index(
                fields=["-created_at"],
                name="idx_txn_created_at",
            ),
            models.Index(
                fields=["sender_account"],
                name="idx_txn_sender",
            ),
            models.Index(
                fields=["receiver_account"],
                name="idx_txn_receiver",
            ),
        ]

    def __str__(self):
        return f"TXN-{self.reference_number}: {self.amount} {self.currency_id}"

    def get_absolute_url(self):
        return reverse(
            "admin:transactions_transaction_change",
            args=[self.pk],
        )

    def clean(self):
        super().clean()
        if not self.sender_account and not self.receiver_account:
            raise ValidationError("At least one of sender or receiver account must be specified.")

    def can_transition_to(self, new_status: str) -> bool:
        """Check if transition to new_status is allowed."""
        allowed = self.ALLOWED_TRANSITIONS.get(self.status, [])
        return new_status in allowed

    def transition_to(self, new_status: str) -> None:
        """
        Transition the transaction to a new status.

        Raises ValidationError if the transition is not allowed.
        """
        if not self.can_transition_to(new_status):
            raise ValidationError(
                f"Cannot transition transaction from {self.status} to {new_status}."
            )
        self.status = new_status
        self.save(update_fields=["status", "updated_at"])
