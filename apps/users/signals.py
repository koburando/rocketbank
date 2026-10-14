"""
Signals for the Users app.

Auto-creates Profile and welcome Notification when a User is created.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import Profile, User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create a Profile when a new User is registered."""
    if created:
        Profile.objects.create(user=instance)
        logger.info("Created profile for user %s", instance.email)


@receiver(post_save, sender=User)
def create_welcome_notification(sender, instance, created, **kwargs):
    """Send a welcome notification when a new User is registered."""
    if created:
        # Lazy import to avoid circular dependency
        from apps.notifications.models import Notification

        Notification.objects.create(
            user=instance,
            title="Welcome to RocketBank!",
            message=(
                f"Hello {instance.get_full_name() or instance.username}, "
                "welcome to RocketBank! Start by setting up your profile "
                "and opening your first bank account."
            ),
            notification_type=Notification.NotificationType.INFO,
        )
        logger.info(
            "Created welcome notification for user %s",
            instance.email,
        )
