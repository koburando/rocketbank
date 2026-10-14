"""
Domain models for the Support app.

Provides FAQ, SupportTicket, and TicketReview models
for customer support and feedback management.
"""

from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_rating


class FAQ(TimeStampedModel):
    """Frequently Asked Question for self-service support."""

    question = models.CharField("question", max_length=500)
    answer = models.TextField("answer")
    category = models.CharField("category", max_length=100)
    order = models.PositiveIntegerField("display order", default=0)
    is_published = models.BooleanField("published", default=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["category", "order"]

    def __str__(self):
        return self.question[:80]

    def get_absolute_url(self):
        return reverse("admin:support_faq_change", args=[self.pk])


class SupportTicket(TimeStampedModel):
    """Customer support ticket with status and priority tracking."""

    class TicketStatus(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        WAITING_CUSTOMER = "WAITING", "Waiting on Customer"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    class TicketPriority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="support_tickets",
        verbose_name="user",
    )
    subject = models.CharField("subject", max_length=300)
    description = models.TextField("description")
    status = models.CharField(
        "status",
        max_length=15,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN,
    )
    priority = models.CharField(
        "priority",
        max_length=10,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM,
    )
    assigned_to = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
        verbose_name="assigned to",
    )

    class Meta:
        verbose_name = "support ticket"
        verbose_name_plural = "support tickets"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"], name="idx_ticket_status"),
            models.Index(fields=["priority"], name="idx_ticket_priority"),
        ]

    def __str__(self):
        return f"Ticket #{self.pk}: {self.subject[:50]}"

    def get_absolute_url(self):
        return reverse("admin:support_supportticket_change", args=[self.pk])


class TicketReview(TimeStampedModel):
    """Review/rating for a support ticket interaction."""

    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="ticket",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="ticket_reviews",
        verbose_name="user",
    )
    rating = models.PositiveSmallIntegerField(
        "rating",
        validators=[validate_rating],
        help_text="Rating from 1 (poor) to 5 (excellent)",
    )
    comment = models.TextField("comment", blank=True)
    is_helpful_count = models.PositiveIntegerField(
        "helpful votes",
        default=0,
    )

    class Meta:
        verbose_name = "ticket review"
        verbose_name_plural = "ticket reviews"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name="support_rating_range",
            ),
        ]

    def __str__(self):
        return f"Review by {self.user.email} — {self.rating}/5"

    def get_absolute_url(self):
        return reverse("admin:support_ticketreview_change", args=[self.pk])
