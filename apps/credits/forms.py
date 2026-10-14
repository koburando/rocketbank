"""
Forms for the Credits app: Loan Calculator and Loan Application ModelForm.
"""

from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from apps.credits.models import LoanApplication, LoanProduct


class LoanCalculatorForm(forms.Form):
    """
    Form for simulating loan monthly payments and amortization.
    """

    product = forms.ModelChoiceField(
        label="Loan Product",
        queryset=LoanProduct.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-select", "id": "calc_product"}),
    )
    amount = forms.DecimalField(
        label="Desired Loan Amount (KZT)",
        max_digits=12,
        decimal_places=2,
        initial=Decimal("1000000.00"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-input font-mono",
                "step": "50000",
                "min": "100000",
                "required": "required",
            }
        ),
    )
    term_months = forms.IntegerField(
        label="Term in Months",
        initial=24,
        min_value=3,
        max_value=84,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input font-mono",
                "step": "6",
                "required": "required",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        amount = cleaned_data.get("amount")
        term_months = cleaned_data.get("term_months")

        if product and amount:
            if not (product.min_amount <= amount <= product.max_amount):
                raise ValidationError(
                    f"For {product.title}, the amount must be between "
                    f"{product.min_amount:,.0f} and {product.max_amount:,.0f} KZT."
                )

        if product and term_months:
            if not (product.min_term_months <= term_months <= product.max_term_months):
                raise ValidationError(
                    f"For {product.title}, the term must be between "
                    f"{product.min_term_months} and {product.max_term_months} months."
                )

        return cleaned_data


class LoanApplicationForm(forms.ModelForm):
    """
    ModelForm for submitting a consumer credit application.
    Enforces product constraints and debt-to-income ratios.
    """

    product = forms.ModelChoiceField(
        label="Loan Product",
        queryset=LoanProduct.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-select", "required": "required"}),
    )
    requested_amount = forms.DecimalField(
        label="Requested Loan Amount (KZT)",
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input font-mono",
                "placeholder": "e.g. 1500000",
                "step": "10000",
                "required": "required",
            }
        ),
    )
    term_months = forms.IntegerField(
        label="Repayment Term (Months)",
        widget=forms.NumberInput(
            attrs={
                "class": "form-input font-mono",
                "placeholder": "e.g. 24",
                "step": "6",
                "required": "required",
            }
        ),
    )
    monthly_income = forms.DecimalField(
        label="Verified Monthly Net Income (KZT)",
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input font-mono",
                "placeholder": "e.g. 350000",
                "required": "required",
            }
        ),
        help_text="Your regular monthly earnings after taxes.",
    )
    consent_credit_bureau = forms.BooleanField(
        label=(
            "I authorize RocketBank to retrieve my credit history from "
            "the State Credit Bureau (GKB)."
        ),
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = LoanApplication
        fields = [
            "product",
            "requested_amount",
            "term_months",
            "monthly_income",
        ]

    def clean_requested_amount(self):
        amount = self.cleaned_data.get("requested_amount")
        if amount is not None and amount <= 0:
            raise ValidationError("Requested amount must be positive.")
        return amount

    def clean_term_months(self):
        term = self.cleaned_data.get("term_months")
        if term is not None and term < 1:
            raise ValidationError("Loan term must be at least 1 month.")
        return term

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        amount = cleaned_data.get("requested_amount")
        term = cleaned_data.get("term_months")
        income = cleaned_data.get("monthly_income")

        if product and amount:
            if not (product.min_amount <= amount <= product.max_amount):
                self.add_error(
                    "requested_amount",
                    f"Amount must be between {product.min_amount:,.0f} and "
                    f"{product.max_amount:,.0f} KZT.",
                )

        if product and term:
            if not (product.min_term_months <= term <= product.max_term_months):
                self.add_error(
                    "term_months",
                    f"Term must be between {product.min_term_months} and "
                    f"{product.max_term_months} months.",
                )

        # Cross-field: Debt-to-income feasibility
        if amount and term and income and product:
            monthly_rate = (product.interest_rate / Decimal("100")) / Decimal("12")
            if monthly_rate > 0:
                power = (1 + monthly_rate) ** term
                annuity_factor = (monthly_rate * power) / (power - 1)
                est_monthly_payment = amount * annuity_factor
            else:
                est_monthly_payment = amount / term

            # If payment is > 50% of monthly income, warn or reject
            if est_monthly_payment > (income * Decimal("0.50")):
                raise ValidationError(
                    f"Estimated monthly payment ({est_monthly_payment:,.0f} KZT) exceeds 50% "
                    f"of your declared monthly income ({income:,.0f} KZT). "
                    "Please reduce the amount or extend the term."
                )

        return cleaned_data
