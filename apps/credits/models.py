"""
Domain models for the Credits app.

Provides LoanProduct catalog, LoanApplication with status workflow,
and LoanSchedule for amortization tracking.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class LoanProduct(TimeStampedModel):
    """Loan product catalog with terms and interest rates."""

    title = models.CharField("title", max_length=200)
    slug = models.SlugField("slug", unique=True)
    min_amount = models.DecimalField(
        "minimum amount",
        max_digits=12,
        decimal_places=2,
    )
    max_amount = models.DecimalField(
        "maximum amount",
        max_digits=12,
        decimal_places=2,
    )
    interest_rate = models.DecimalField(
        "annual interest rate (%)",
        max_digits=5,
        decimal_places=2,
    )
    min_term_months = models.PositiveIntegerField(
        "minimum term (months)",
    )
    max_term_months = models.PositiveIntegerField(
        "maximum term (months)",
    )
    is_active = models.BooleanField("active", default=True)
    description = models.TextField("description", blank=True)

    class Meta:
        verbose_name = "loan product"
        verbose_name_plural = "loan products"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.interest_rate}%)"

    def get_absolute_url(self):
        return reverse("admin:credits_loanproduct_change", args=[self.pk])

    def clean(self):
        super().clean()
        if (
            self.min_amount is not None
            and self.max_amount is not None
            and self.min_amount >= self.max_amount
        ):
            raise ValidationError("Minimum amount must be less than maximum amount.")
        if (
            self.min_term_months is not None
            and self.max_term_months is not None
            and self.min_term_months >= self.max_term_months
        ):
            raise ValidationError("Minimum term must be less than maximum term.")


class LoanApplication(TimeStampedModel):
    """
    Loan application submitted by a user for a specific product.

    Follows a status workflow: DRAFT → SUBMITTED → UNDER_REVIEW →
    APPROVED/REJECTED → DISBURSED → CLOSED.
    """

    class LoanStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        DISBURSED = "DISBURSED", "Disbursed"
        CLOSED = "CLOSED", "Closed"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="loan_applications",
        verbose_name="user",
    )
    product = models.ForeignKey(
        LoanProduct,
        on_delete=models.PROTECT,
        related_name="applications",
        verbose_name="loan product",
    )
    requested_amount = models.DecimalField(
        "requested amount",
        max_digits=12,
        decimal_places=2,
    )
    term_months = models.PositiveIntegerField("term (months)")
    status = models.CharField(
        "status",
        max_length=15,
        choices=LoanStatus.choices,
        default=LoanStatus.DRAFT,
    )
    monthly_income = models.DecimalField(
        "monthly income",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    approved_at = models.DateTimeField(
        "approved at",
        null=True,
        blank=True,
    )
    rejection_reason = models.TextField(
        "rejection reason",
        blank=True,
    )

    class Meta:
        verbose_name = "loan application"
        verbose_name_plural = "loan applications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Loan #{self.pk} — {self.requested_amount} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse(
            "admin:credits_loanapplication_change",
            args=[self.pk],
        )

    def clean(self):
        super().clean()
        if self.product_id:
            product = self.product
            if not (product.min_amount <= self.requested_amount <= product.max_amount):
                raise ValidationError(
                    f"Requested amount must be between "
                    f"{product.min_amount} and {product.max_amount}."
                )
            if not (product.min_term_months <= self.term_months <= product.max_term_months):
                raise ValidationError(
                    f"Term must be between "
                    f"{product.min_term_months} and "
                    f"{product.max_term_months} months."
                )


class LoanSchedule(TimeStampedModel):
    """Amortization schedule entry for a loan application."""

    loan = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name="schedule_entries",
        verbose_name="loan",
    )
    installment_number = models.PositiveIntegerField(
        "installment #",
    )
    due_date = models.DateField("due date")
    principal_amount = models.DecimalField(
        "principal",
        max_digits=12,
        decimal_places=2,
    )
    interest_amount = models.DecimalField(
        "interest",
        max_digits=12,
        decimal_places=2,
    )
    is_paid = models.BooleanField("paid", default=False)
    paid_at = models.DateTimeField(
        "paid at",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "loan schedule entry"
        verbose_name_plural = "loan schedule entries"
        ordering = ["loan", "installment_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["loan", "installment_number"],
                name="unique_loan_installment",
            ),
        ]

    def __str__(self):
        return f"Installment #{self.installment_number} for Loan #{self.loan_id}"

    def get_absolute_url(self):
        return reverse("admin:credits_loanschedule_change", args=[self.pk])

    @property
    def total_amount(self):
        """Total payment = principal + interest."""
        return self.principal_amount + self.interest_amount
