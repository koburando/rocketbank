"""
Signals for file cleanup and media management.
Automatically deletes obsolete and deleted files from storage.
"""

from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


def delete_file_from_storage(storage, name):
    """Helper to safely delete a file from storage without raising."""
    if name and storage.exists(name):
        try:
            storage.delete(name)
        except Exception:
            pass


@receiver(pre_save)
def auto_delete_old_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem/storage when corresponding FileField/ImageField is updated.
    """
    if sender._meta.app_label not in (
        "users",
        "core",
        "accounts",
        "cards",
        "credits",
        "deposits",
        "support",
    ):
        return

    file_fields = [f for f in sender._meta.get_fields() if isinstance(f, models.FileField)]
    if not file_fields or not instance.pk:
        return

    try:
        old_instance = sender.objects.filter(pk=instance.pk).first()
        if not old_instance:
            return
    except Exception:
        return

    for field in file_fields:
        old_file = getattr(old_instance, field.name, None)
        new_file = getattr(instance, field.name, None)

        if (
            old_file
            and old_file.name
            and (not new_file or old_file.name != getattr(new_file, "name", None))
        ):
            delete_file_from_storage(old_file.storage, old_file.name)


@receiver(post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem/storage when corresponding model record is deleted.
    """
    if sender._meta.app_label not in (
        "users",
        "core",
        "accounts",
        "cards",
        "credits",
        "deposits",
        "support",
    ):
        return

    file_fields = [f for f in sender._meta.get_fields() if isinstance(f, models.FileField)]
    for field in file_fields:
        file = getattr(instance, field.name, None)
        if file and file.name:
            delete_file_from_storage(file.storage, file.name)
