"""
Forms for the Support app: SupportTicketForm and TicketReviewForm.
"""

from django import forms
from django.core.exceptions import ValidationError

from apps.support.models import SupportTicket, TicketReview


class SupportTicketForm(forms.ModelForm):
    """
    ModelForm for customer support ticket creation with field validation.
    """

    class Meta:
        model = SupportTicket
        fields = ["subject", "description", "priority"]
        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Brief summary of the inquiry or issue",
                    "required": "required",
                    "minlength": "5",
                    "maxlength": "300",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 5,
                    "placeholder": (
                        "Please provide detailed steps, error messages, "
                        "or affected account numbers..."
                    ),
                    "required": "required",
                    "minlength": "15",
                }
            ),
            "priority": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_subject(self):
        subject = self.cleaned_data.get("subject", "").strip()
        if len(subject) < 5:
            raise ValidationError("Subject must be at least 5 characters long.")
        return subject

    def clean_description(self):
        desc = self.cleaned_data.get("description", "").strip()
        if len(desc) < 15:
            raise ValidationError(
                "Please provide a more detailed description (at least 15 characters)."
            )
        return desc


class TicketReviewForm(forms.ModelForm):
    """
    Form for rating support ticket assistance (1 to 5).
    """

    class Meta:
        model = TicketReview
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                choices=[
                    (5, "⭐⭐⭐⭐⭐ 5 - Excellent"),
                    (4, "⭐⭐⭐⭐ 4 - Good"),
                    (3, "⭐⭐⭐ 3 - Average"),
                    (2, "⭐⭐ 2 - Poor"),
                    (1, "⭐ 1 - Terrible"),
                ],
                attrs={"class": "form-select", "required": "required"},
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 3,
                    "placeholder": "Tell us how we can improve our service (optional)...",
                }
            ),
        }
