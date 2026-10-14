"""
Custom exception handler for unified JSON error responses across the REST API.
Handles 400, 401, 403, 404, 429, and 500 status codes consistently.
"""

import logging

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def _extract_error_message(error_data) -> str:
    """Build clean user-facing error message from error_data."""
    if isinstance(error_data, dict):
        if "detail" in error_data:
            return str(error_data["detail"])
        if "non_field_errors" in error_data:
            items = error_data["non_field_errors"]
            return " ".join([str(e) for e in items]) if isinstance(items, list) else str(items)
        first_key = next(iter(error_data.keys()))
        val = error_data[first_key]
        first_val = val[0] if isinstance(val, (list, tuple)) and val else val
        return f"{first_key}: {first_val}"
    if isinstance(error_data, list):
        return " ".join([str(e) for e in error_data])
    return "An error occurred while processing your request."


def custom_exception_handler(exc, context):
    """
    Returns a unified JSON error payload:
    {
        "status": "error",
        "code": 404,
        "message": "Not found.",
        "errors": { ... }
    }
    """
    # Convert Django standard exceptions to DRF exceptions if needed
    if isinstance(exc, Http404):
        exc = drf_exceptions.NotFound(*(exc.args))
    elif isinstance(exc, PermissionDenied):
        exc = drf_exceptions.PermissionDenied(*(exc.args))
    elif isinstance(exc, DjangoValidationError):
        if hasattr(exc, "message_dict"):
            exc = drf_exceptions.ValidationError(detail=exc.message_dict)
        elif hasattr(exc, "messages"):
            exc = drf_exceptions.ValidationError(detail=exc.messages)
        else:
            exc = drf_exceptions.ValidationError(detail=str(exc))

    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code
        error_data = response.data
        message = _extract_error_message(error_data)

        unified_payload = {
            "status": "error",
            "code": status_code,
            "message": message,
            "errors": error_data,
        }

        response.data = unified_payload
    else:
        logger.exception("Unhandled REST API exception in context %s", context, exc_info=exc)

    return response
