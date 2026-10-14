"""
Domain models for the Analytics app.

Provides SavingGoal for tracking user financial goals
with progress calculation.
"""

from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel


class SavingGoal(TimeStampedModel):
    """
    A financial saving goal set by the user.

    Tracks target amount, current progress, and deadline.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="saving_goals",
        verbose_name="user",
    )
    title = models.CharField("title", max_length=200)
    target_amount = models.DecimalField(
        "target amount",
        max_digits=15,
        decimal_places=2,
    )
    current_amount = models.DecimalField(
        "current amount",
        max_digits=15,
        decimal_places=2,
        default=0,
    )
    deadline = models.DateField(
        "deadline",
        null=True,
        blank=True,
    )
    category = models.CharField(
        "category",
        max_length=50,
        blank=True,
        help_text="e.g. vacation, car, house, education",
    )
    is_achieved = models.BooleanField("achieved", default=False)

    class Meta:
        verbose_name = "saving goal"
        verbose_name_plural = "saving goals"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.progress_percent:.0f}%)"

    def get_absolute_url(self):
        return reverse(
            "admin:analytics_savinggoal_change", args=[self.pk]
        )

    @property
    def progress_percent(self):
        """Return progress as percentage, capped at 100%."""
        if not self.target_amount:
            return 0
        pct = (self.current_amount / self.target_amount) * 100
        return min(pct, 100)
