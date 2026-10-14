"""
Custom URL path converters for RocketBank.
"""

from django.urls import register_converter


class IBANConverter:
    """Path converter for IBAN account identifiers."""

    regex = r"[A-Z]{2}[0-9]{2}[A-Za-z0-9]{12,30}"

    def to_python(self, value: str) -> str:
        return value.strip()

    def to_url(self, value: str) -> str:
        return str(value)


class ReferenceConverter:
    """Path converter for transaction reference numbers (e.g., TXN-ABC123XYZ)."""

    regex = r"TXN-[A-Za-z0-9]+"

    def to_python(self, value: str) -> str:
        return value.strip()

    def to_url(self, value: str) -> str:
        return str(value)


def register_custom_converters():
    """Register all custom path converters."""
    register_converter(IBANConverter, "iban")
    register_converter(ReferenceConverter, "ref")
