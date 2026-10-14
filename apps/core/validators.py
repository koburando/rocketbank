"""
Custom validators for RocketBank domain models.

Provides reusable validation logic for IBANs, ratings,
phone numbers, and other domain-specific fields.
"""

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_iban(value: str) -> None:
    """
    Validate IBAN format.

    IBAN consists of a 2-letter country code, 2 check digits,
    and a BBAN of up to 30 alphanumeric characters (total 15-34 chars).
    """
    pattern = r"^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$"
    if not re.match(pattern, value.upper().replace(" ", "")):
        raise ValidationError(
            _("%(value)s is not a valid IBAN format."),
            code="invalid_iban",
            params={"value": value},
        )


def validate_rating(value: int) -> None:
    """Validate that a rating is between 1 and 5 (inclusive)."""
    if not 1 <= value <= 5:
        raise ValidationError(
            _("Rating must be between 1 and 5. Got %(value)s."),
            code="invalid_rating",
            params={"value": value},
        )


def validate_phone_number(value: str) -> None:
    """
    Validate phone number format.

    Accepts formats like: +7XXXXXXXXXX, +1XXXXXXXXXX, etc.
    """
    pattern = r"^\+?[1-9]\d{6,14}$"
    if not re.match(pattern, value.replace(" ", "").replace("-", "")):
        raise ValidationError(
            _("%(value)s is not a valid phone number."),
            code="invalid_phone",
            params={"value": value},
        )
