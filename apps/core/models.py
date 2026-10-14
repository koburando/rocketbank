"""
Abstract base models for RocketBank.

Provides TimeStampedModel and SoftDeleteModel with custom managers
for consistent timestamp tracking and soft-delete functionality
across all domain models.
"""

from django.db import models
from django.utils import timezone

# ──────────────────────────────────────────────
# Custom Managers
# ──────────────────────────────────────────────


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet that supports soft-delete filtering."""

    def active(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)

    def soft_delete(self):
        return self.update(is_deleted=True, deleted_at=timezone.now())

    def restore(self):
        return self.update(is_deleted=False, deleted_at=None)


class SoftDeleteManager(models.Manager):
    """Default manager that excludes soft-deleted records."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).active()

    def active(self):
        return self.get_queryset()

    def deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db).deleted()


class AllObjectsManager(models.Manager):
    """Manager that includes ALL records, including soft-deleted."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


# ──────────────────────────────────────────────
# Abstract Models
# ──────────────────────────────────────────────


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(
        "created at",
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        "updated at",
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SoftDeleteModel(TimeStampedModel):
    """
    Abstract model providing soft-delete functionality.

    Uses ``SoftDeleteManager`` as default manager (excludes deleted),
    and ``all_objects`` manager to include soft-deleted records.
    """

    is_deleted = models.BooleanField(
        "deleted",
        default=False,
        db_index=True,
    )
    deleted_at = models.DateTimeField(
        "deleted at",
        null=True,
        blank=True,
    )

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self):
        """Mark this record as deleted without removing from DB."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    def restore(self):
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])
