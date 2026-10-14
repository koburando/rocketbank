"""
Domain models for the Cards app.

Provides CardProduct catalog and BankCard with state-machine
transition logic for card lifecycle management.
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


# ──────────────────────────────────────────────
# Custom Managers
# ──────────────────────────────────────────────


class CardProductQuerySet(models.QuerySet):
    """QuerySet for CardProduct with business filters."""

    def active(self):
        return self.filter(is_active=True)

    def popular(self):
        """Order by number of issued cards (descending)."""
        return self.annotate(
            card_count=models.Count("issued_cards")
        ).order_by("-card_count")


class CardProductManager(models.Manager):
    """Manager for CardProduct."""

    def get_queryset(self):
        return CardProductQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def popular(self):
        return self.get_queryset().popular()


# ──────────────────────────────────────────────
# Models
# ──────────────────────────────────────────────


class CardProduct(TimeStampedModel):
    """Card product catalog (Standard, Gold, Platinum, Black)."""

    class CardTier(models.TextChoices):
        STANDARD = "STANDARD", "Standard"
        GOLD = "GOLD", "Gold"
        PLATINUM = "PLATINUM", "Platinum"
        BLACK = "BLACK", "Black"

    slug = models.SlugField("slug", unique=True)
    title = models.CharField("title", max_length=100)
    tier = models.CharField(
        "tier",
        max_length=10,
        choices=CardTier.choices,
        default=CardTier.STANDARD,
    )
    cashback_percent = models.DecimalField(
        "cashback %",
        max_digits=4,
        decimal_places=2,
        default=0,
    )
    annual_fee = models.DecimalField(
        "annual fee",
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    description = models.TextField("description", blank=True)
    is_active = models.BooleanField("active", default=True)

    objects = CardProductManager()

    class Meta:
        verbose_name = "card product"
        verbose_name_plural = "card products"
        ordering = ["tier"]

    def __str__(self):
        return f"{self.title} ({self.get_tier_display()})"

    def get_absolute_url(self):
        return reverse(
            "admin:cards_cardproduct_change", args=[self.pk]
        )


class BankCard(TimeStampedModel):
    """
    Issued bank card linked to an account and product.

    Includes state-machine transition logic for card lifecycle:
    ACTIVE → BLOCKED / EXPIRED / CANCELLED
    BLOCKED → ACTIVE / CANCELLED
    EXPIRED → CANCELLED
    CANCELLED → (terminal)
    """

    class CardStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        BLOCKED = "BLOCKED", "Blocked"
        EXPIRED = "EXPIRED", "Expired"
        CANCELLED = "CANCELLED", "Cancelled"

    ALLOWED_TRANSITIONS = {
        CardStatus.ACTIVE: [
            CardStatus.BLOCKED,
            CardStatus.EXPIRED,
            CardStatus.CANCELLED,
        ],
        CardStatus.BLOCKED: [
            CardStatus.ACTIVE,
            CardStatus.CANCELLED,
        ],
        CardStatus.EXPIRED: [CardStatus.CANCELLED],
        CardStatus.CANCELLED: [],
    }

    account = models.ForeignKey(
        "accounts.BankAccount",
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name="account",
    )
    product = models.ForeignKey(
        CardProduct,
        on_delete=models.PROTECT,
        related_name="issued_cards",
        verbose_name="product",
    )
    card_number_masked = models.CharField(
        "masked card number",
        max_length=19,
        help_text="e.g. **** **** **** 1234",
    )
    expiry_date = models.DateField("expiry date")
    status = models.CharField(
        "status",
        max_length=10,
        choices=CardStatus.choices,
        default=CardStatus.ACTIVE,
    )
    daily_limit = models.DecimalField(
        "daily limit",
        max_digits=12,
        decimal_places=2,
        default=500_000,
    )
    issued_at = models.DateTimeField(
        "issued at", auto_now_add=True
    )

    class Meta:
        verbose_name = "bank card"
        verbose_name_plural = "bank cards"
        ordering = ["-issued_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["account", "card_number_masked"],
                name="unique_card_per_account",
            ),
        ]
        indexes = [
            models.Index(
                fields=["status"], name="idx_card_status"
            ),
        ]

    def __str__(self):
        return (
            f"{self.card_number_masked} "
            f"({self.get_status_display()})"
        )

    def get_absolute_url(self):
        return reverse(
            "admin:cards_bankcard_change", args=[self.pk]
        )

    def can_transition_to(self, new_status: str) -> bool:
        """Check if transition to new_status is allowed."""
        allowed = self.ALLOWED_TRANSITIONS.get(self.status, [])
        return new_status in allowed

    def transition_to(self, new_status: str) -> None:
        """
        Transition the card to a new status.

        Raises ValidationError if the transition is not allowed.
        """
        if not self.can_transition_to(new_status):
            raise ValidationError(
                f"Cannot transition card from "
                f"{self.status} to {new_status}."
            )
        self.status = new_status
        self.save(update_fields=["status", "updated_at"])
