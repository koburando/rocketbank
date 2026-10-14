"""
Domain models for the Notifications app.

Provides Notification model for in-app user notifications
with type categorization and read-tracking.
"""

from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class Notification(TimeStampedModel):
    """In-app notification for a user."""

    class NotificationType(models.TextChoices):
        INFO = "INFO", "Info"
        WARNING = "WARNING", "Warning"
        SUCCESS = "SUCCESS", "Success"
        ERROR = "ERROR", "Error"
        TRANSACTION = "TRANSACTION", "Transaction"
        SECURITY = "SECURITY", "Security"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="user",
    )
    title = models.CharField("title", max_length=200)
    message = models.TextField("message")
    notification_type = models.CharField(
        "type",
        max_length=15,
        choices=NotificationType.choices,
        default=NotificationType.INFO,
    )
    is_read = models.BooleanField(
        "read",
        default=False,
        db_index=True,
    )
    read_at = models.DateTimeField(
        "read at",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "notification"
        verbose_name_plural = "notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["user", "is_read"],
                name="idx_notification_user_read",
            ),
            models.Index(
                fields=["-created_at"],
                name="idx_notification_created",
            ),
        ]

    def __str__(self):
        return f"{self.title} → {self.user.email}"

    def get_absolute_url(self):
        return reverse(
            "admin:notifications_notification_change",
            args=[self.pk],
        )

    def mark_as_read(self):
        """Mark this notification as read."""
        from django.utils import timezone

        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=["is_read", "read_at", "updated_at"])
