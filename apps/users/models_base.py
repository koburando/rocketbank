"""
Abstract base models and managers for RocketBank.

Provides TimeStampedModel and SoftDeleteModel with custom managers
for consistent timestamp tracking and soft-delete functionality.
"""

from apps.core.models import (
    AllObjectsManager,
    SoftDeleteManager,
    SoftDeleteModel,
    SoftDeleteQuerySet,
    TimeStampedModel,
)

__all__ = [
    "TimeStampedModel",
    "SoftDeleteModel",
    "SoftDeleteManager",
    "AllObjectsManager",
    "SoftDeleteQuerySet",
]
