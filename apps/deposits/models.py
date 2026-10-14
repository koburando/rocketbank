"""
Domain models for the Deposits app.

Provides DepositProduct catalog and UserDeposit for tracking
customer fixed-term deposits with interest accrual.
"""

from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class DepositProduct(TimeStampedModel):
    """Deposit product catalog with interest rates and terms."""

    title = models.CharField("title", max_length=200)
    slug = models.SlugField("slug", unique=True)
    interest_rate = models.DecimalField(
        "annual interest rate (%)",
        max_digits=5,
        decimal_places=2,
    )
    min_amount = models.DecimalField(
        "minimum amount",
        max_digits=12,
        decimal_places=2,
    )
    term_months = models.PositiveIntegerField("term (months)")
    is_early_withdrawal_allowed = models.BooleanField(
        "early withdrawal allowed",
        default=False,
    )
    is_active = models.BooleanField("active", default=True)
    description = models.TextField("description", blank=True)

    class Meta:
        verbose_name = "deposit product"
        verbose_name_plural = "deposit products"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.interest_rate}% / {self.term_months}mo)"

    def get_absolute_url(self):
        return reverse(
            "admin:deposits_depositproduct_change",
            args=[self.pk],
        )


class UserDeposit(TimeStampedModel):
    """A customer's active or closed fixed-term deposit."""

    class DepositStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        CLOSED = "CLOSED", "Closed"
        EARLY_CLOSED = "EARLY_CLOSED", "Early Closed"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="deposits",
        verbose_name="user",
    )
    account = models.ForeignKey(
        "accounts.BankAccount",
        on_delete=models.PROTECT,
        related_name="deposits",
        verbose_name="linked account",
    )
    product = models.ForeignKey(
        DepositProduct,
        on_delete=models.PROTECT,
        related_name="user_deposits",
        verbose_name="deposit product",
    )
    amount = models.DecimalField(
        "deposit amount",
        max_digits=15,
        decimal_places=2,
    )
    accrued_interest = models.DecimalField(
        "accrued interest",
        max_digits=15,
        decimal_places=2,
        default=0,
    )
    start_date = models.DateField("start date")
    end_date = models.DateField("end date")
    status = models.CharField(
        "status",
        max_length=15,
        choices=DepositStatus.choices,
        default=DepositStatus.ACTIVE,
    )

    class Meta:
        verbose_name = "user deposit"
        verbose_name_plural = "user deposits"
        ordering = ["-start_date"]

    def __str__(self):
        return f"Deposit {self.product.title} — {self.amount} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse("admin:deposits_userdeposit_change", args=[self.pk])
