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


def validate_image_file(file):
    """
    Validate uploaded image file:
    - Maximum file size (5MB)
    - Allowed extensions (.jpg, .jpeg, .png, .webp, .gif)
    - Valid image MIME type
    - Image dimensions (min 32x32, max 4096x4096)
    """
    from pathlib import Path

    from PIL import Image

    max_size_mb = 5
    max_size_bytes = max_size_mb * 1024 * 1024
    if file.size > max_size_bytes:
        size_mb = file.size / (1024 * 1024)
        raise ValidationError(
            _("Image file size cannot exceed %(max)s MB. Got %(actual).1f MB.")
            % {"max": max_size_mb, "actual": size_mb},
            code="file_too_large",
        )

    allowed_extensions = {".jpeg", ".jpg", ".png", ".gif", ".webp"}
    ext = Path(file.name).suffix.lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            _(f"Unsupported file extension '{ext}'. Allowed: {', '.join(allowed_extensions)}"),
            code="invalid_extension",
        )

    content_type = getattr(file, "content_type", None)
    allowed_mimes = {"image/webp", "image/gif", "image/jpeg", "image/png"}
    if content_type and content_type.lower() not in allowed_mimes:
        raise ValidationError(
            _(f"Invalid MIME type '{content_type}'. Must be an image."),
            code="invalid_mime_type",
        )

    try:
        file.seek(0)
        with Image.open(file) as img:
            img.verify()

        file.seek(0)
        with Image.open(file) as img:
            width, height = img.size
            if width < 32 or height < 32:
                raise ValidationError(
                    _(f"Image dimensions too small ({width}x{height}px). Minimum is 32x32px."),
                    code="image_too_small",
                )
            if width > 4096 or height > 4096:
                raise ValidationError(
                    _(f"Image dimensions too large ({width}x{height}px). Maximum is 4096x4096px."),
                    code="image_too_large",
                )
        file.seek(0)
    except ValidationError:
        raise
    except Exception as exc:
        raise ValidationError(
            _(f"Invalid or corrupted image file: {exc}"),
            code="corrupt_image",
        ) from exc
