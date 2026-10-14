"""
Signals for the Transactions app.

Sends notifications to sender/receiver when a transaction completes.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.transactions.models import Transaction

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Transaction)
def notify_transaction_parties(sender, instance, created, **kwargs):
    """Create notifications for transaction parties on completion."""
    if instance.status != Transaction.TransactionStatus.COMPLETED:
        return

    # Lazy import to avoid circular dependency
    from apps.notifications.models import Notification

    if instance.sender_account:
        Notification.objects.create(
            user=instance.sender_account.owner,
            title="Money Sent",
            message=(
                f"You sent {instance.amount} {instance.currency_id} "
                f"(Ref: {instance.reference_number})."
            ),
            notification_type=Notification.NotificationType.TRANSACTION,
        )
        logger.info(
            "Sent debit notification for TXN %s",
            instance.reference_number,
        )

    if instance.receiver_account:
        Notification.objects.create(
            user=instance.receiver_account.owner,
            title="Money Received",
            message=(
                f"You received {instance.amount} "
                f"{instance.currency_id} "
                f"(Ref: {instance.reference_number})."
            ),
            notification_type=Notification.NotificationType.TRANSACTION,
        )
        logger.info(
            "Sent credit notification for TXN %s",
            instance.reference_number,
        )
