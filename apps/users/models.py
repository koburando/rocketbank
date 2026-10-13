import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


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
