import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_image_file


class User(AbstractUser):
    """Custom User model for RocketBank with UUID primary key."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        "email address",
        unique=True,
    )
    phone_number = models.CharField(
        "phone number",
        max_length=20,
        blank=True,
    )
    is_verified = models.BooleanField(
        "verified",
        default=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("admin:users_user_change", args=[self.pk])


class Profile(TimeStampedModel):
    """Extended user profile with KYC, preferences, and personal info."""

    class KYCStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    class ThemeChoice(models.TextChoices):
        LIGHT = "LIGHT", "Light"
        DARK = "DARK", "Dark"
        SYSTEM = "SYSTEM", "System"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="user",
    )
    avatar = models.ImageField(
        "avatar",
        upload_to="avatars/",
        blank=True,
        validators=[validate_image_file],
    )
    birth_date = models.DateField(
        "birth date",
        null=True,
        blank=True,
    )
    address = models.TextField(
        "address",
        blank=True,
    )
    kyc_status = models.CharField(
        "KYC status",
        max_length=10,
        choices=KYCStatus.choices,
        default=KYCStatus.PENDING,
    )
    preferred_theme = models.CharField(
        "preferred theme",
        max_length=10,
        choices=ThemeChoice.choices,
        default=ThemeChoice.SYSTEM,
    )
    preferred_language = models.CharField(
        "preferred language",
        max_length=10,
        default="en",
    )

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        ordering = ["-created_at"]

    @property
    def theme_preference(self):
        return self.preferred_theme

    @theme_preference.setter
    def theme_preference(self, value):
        self.preferred_theme = value

    def __str__(self):
        return f"Profile of {self.user.email}"

    def get_absolute_url(self):
        return reverse("admin:users_profile_change", args=[self.pk])


class UserFavorite(TimeStampedModel):
    """Favorite financial products (cards, loans, deposits) saved by authenticated user."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="user",
    )
    item_type = models.CharField(
        "item type",
        max_length=50,
        help_text="e.g. card, loan, deposit",
    )
    item_id = models.CharField(
        "item identifier",
        max_length=100,
        help_text="slug or ID of the product",
    )

    class Meta:
        verbose_name = "user favorite"
        verbose_name_plural = "user favorites"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "item_type", "item_id"],
                name="unique_user_favorite_item",
            ),
        ]

    def __str__(self):
        return f"{self.user.email} ★ {self.item_type}:{self.item_id}"


class LoginAudit(TimeStampedModel):
    """Tracks user login history with IP and user agent info."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="login_audits",
        verbose_name="user",
    )
    ip_address = models.GenericIPAddressField("IP address")
    user_agent = models.TextField("user agent", blank=True)
    login_successful = models.BooleanField(
        "login successful",
        default=True,
    )
    location = models.CharField(
        "location",
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = "login audit"
        verbose_name_plural = "login audits"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["user", "-created_at"],
                name="idx_login_audit_user_date",
            ),
        ]

    def __str__(self):
        status = "Success" if self.login_successful else "Failed"
        return f"{self.user.email} — {status} @ {self.ip_address}"

    def get_absolute_url(self):
        return reverse("admin:users_loginaudit_change", args=[self.pk])
