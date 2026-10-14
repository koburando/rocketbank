"""
Business logic / service layer for the Transactions app.

Handles atomic money transfers with race-condition prevention
using select_for_update().
"""

import logging
import uuid

from django.db import transaction as db_transaction

from apps.accounts.models import BankAccount
from apps.transactions.models import Transaction

logger = logging.getLogger(__name__)


def generate_reference_number() -> str:
    """Generate a unique transaction reference number."""
    return f"TXN-{uuid.uuid4().hex[:12].upper()}"


@db_transaction.atomic
def execute_transfer(
    sender_account_id,
    receiver_account_id,
    amount,
    currency_code: str = "KZT",
    description: str = "",
    category=None,
) -> Transaction:
    """
    Execute an atomic money transfer between two accounts.

    Uses select_for_update() to prevent race conditions on concurrent
    balance modifications. Both accounts are locked in a consistent
    order (by PK) to prevent deadlocks.

    Args:
        sender_account_id: UUID of the sender's bank account.
        receiver_account_id: UUID of the receiver's bank account.
        amount: Decimal amount to transfer.
        currency_code: Currency code for the transaction.
        description: Optional description.
        category: Optional TransactionCategory instance.

    Returns:
        The completed Transaction instance.

    Raises:
        ValueError: If sender has insufficient funds or accounts
                    are the same.
    """
    from apps.accounts.models import Currency

    if str(sender_account_id) == str(receiver_account_id):
        raise ValueError("Cannot transfer to the same account.")

    # Lock accounts in consistent order to prevent deadlocks
    ordered_ids = sorted(
        [str(sender_account_id), str(receiver_account_id)]
    )
    accounts = (
        BankAccount.all_objects.filter(id__in=ordered_ids)
        .select_for_update()
        .select_related("currency")
    )

    account_map = {str(a.id): a for a in accounts}
    sender = account_map.get(str(sender_account_id))
    receiver = account_map.get(str(receiver_account_id))

    if not sender or not receiver:
        raise ValueError("One or both accounts not found.")

    if sender.status != BankAccount.AccountStatus.ACTIVE:
        raise ValueError("Sender account is not active.")
    if receiver.status != BankAccount.AccountStatus.ACTIVE:
        raise ValueError("Receiver account is not active.")

    if sender.balance < amount:
        raise ValueError(
            f"Insufficient funds: {sender.balance} < {amount}"
        )

    currency = Currency.objects.get(code=currency_code)

    # Debit sender, credit receiver
    sender.balance -= amount
    sender.save(update_fields=["balance", "updated_at"])

    receiver.balance += amount
    receiver.save(update_fields=["balance", "updated_at"])

    # Create transaction record
    txn = Transaction.objects.create(
        sender_account=sender,
        receiver_account=receiver,
        amount=amount,
        currency=currency,
        status=Transaction.TransactionStatus.COMPLETED,
        transaction_type=Transaction.TransactionType.TRANSFER,
        description=description,
        reference_number=generate_reference_number(),
        category=category,
    )

    logger.info(
        "Transfer %s %s from %s to %s — Ref: %s",
        amount,
        currency_code,
        sender.iban,
        receiver.iban,
        txn.reference_number,
    )
    return txn
