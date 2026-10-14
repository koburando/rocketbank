"""
Forms for the Cards app, including 3-step Card Application Wizard forms.
"""

from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from apps.accounts.models import BankAccount
from apps.cards.models import CardProduct


class CardWizardStep1Form(forms.Form):
    """Step 1: Choose Card Product & Tier."""

    product = forms.ModelChoiceField(
        label="Select Card Tier",
        queryset=CardProduct.objects.filter(is_active=True),
        empty_label=None,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )


class CardWizardStep2Form(forms.Form):
    """Step 2: Link Bank Account and set Limits."""

    account = forms.ModelChoiceField(
        label="Linked Bank Account",
        queryset=BankAccount.objects.none(),
        widget=forms.Select(attrs={"class": "form-select", "required": "required"}),
    )
    daily_limit = forms.DecimalField(
        label="Daily Spending Limit",
        max_digits=12,
        decimal_places=2,
        initial=Decimal("500000.00"),
        min_value=Decimal("10000.00"),
        max_value=Decimal("10000000.00"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-input font-mono",
                "step": "10000",
                "required": "required",
            }
        ),
        help_text="Security threshold for daily card transactions in account currency.",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["account"].queryset = BankAccount.all_objects.filter(
                owner=user,
                is_deleted=False,
                status=BankAccount.AccountStatus.ACTIVE,
            ).select_related("currency")


class CardWizardStep3Form(forms.Form):
    """Step 3: Cardholder Name, Delivery, and Terms."""

    cardholder_name = forms.CharField(
        label="Cardholder Name (Embossed on Card)",
        max_length=26,
        widget=forms.TextInput(
            attrs={
                "class": "form-input font-mono text-uppercase",
                "placeholder": "FIRSTNAME LASTNAME",
                "pattern": "^[A-Za-z ]+$",
                "required": "required",
            }
        ),
        help_text="Latin letters only, as displayed on your passport.",
    )
    delivery_address = forms.CharField(
        label="Delivery Address",
        widget=forms.Textarea(
            attrs={
                "class": "form-textarea",
                "rows": 3,
                "placeholder": "Full delivery street address, apartment, city, zip code",
                "required": "required",
            }
        ),
    )
    accept_terms = forms.BooleanField(
        label="I accept the Payment Card Service Agreement and Cardholder Rules",
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean_cardholder_name(self):
        name = self.cleaned_data.get("cardholder_name", "").strip().upper()
        if not all(c.isalpha() or c.isspace() for c in name):
            raise ValidationError(
                "Cardholder name must contain only Latin alphabet letters and spaces."
            )
        return name
