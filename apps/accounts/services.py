"""
Business logic / service layer for the Accounts app.

Handles account creation, IBAN generation, and balance operations.
"""

import logging
import random
import string

from django.db import transaction

from apps.accounts.models import BankAccount, Currency

logger = logging.getLogger(__name__)


def generate_iban(country_code: str = "KZ") -> str:
    """
    Generate a random IBAN for the given country code.

    Format: {country_code}{2 check digits}{16 digit BBAN}
    """
    check_digits = f"{random.randint(10, 99)}"
    bban = "".join(random.choices(string.digits, k=16))
    return f"{country_code}{check_digits}{bban}"


def generate_unique_iban(country_code: str = "KZ") -> str:
    """Generate a unique IBAN that doesn't exist in the database."""
    for _ in range(100):
        iban = generate_iban(country_code)
        if not BankAccount.all_objects.filter(iban=iban).exists():
            return iban
    raise RuntimeError("Failed to generate unique IBAN after 100 attempts.")


@transaction.atomic
def create_bank_account(
    owner,
    currency_code: str = "KZT",
    account_type: str = BankAccount.AccountType.CHECKING,
    initial_balance=0,
) -> BankAccount:
    """
    Create a new bank account for a user.

    Args:
        owner: The User instance who owns the account.
        currency_code: ISO 4217 currency code (default: KZT).
        account_type: Type of account (CHECKING, SAVINGS, etc.).
        initial_balance: Starting balance (default: 0).

    Returns:
        The newly created BankAccount instance.
    """
    currency = Currency.objects.get(code=currency_code)
    iban = generate_unique_iban()

    account = BankAccount(
        owner=owner,
        currency=currency,
        iban=iban,
        account_type=account_type,
        balance=initial_balance,
    )
    account.full_clean()
    account.save()

    logger.info(
        "Created %s account %s for user %s",
        account_type,
        iban,
        owner.email,
    )
    return account


@transaction.atomic
def freeze_account(account: BankAccount) -> BankAccount:
    """Freeze a bank account, preventing any transactions."""
    account.status = BankAccount.AccountStatus.FROZEN
    account.save(update_fields=["status", "updated_at"])
    logger.info("Froze account %s", account.iban)
    return account


@transaction.atomic
def close_account(account: BankAccount) -> BankAccount:
    """Close a bank account via soft-delete."""
    account.status = BankAccount.AccountStatus.CLOSED
    account.save(update_fields=["status", "updated_at"])
    account.soft_delete()
    logger.info("Closed account %s", account.iban)
    return account
