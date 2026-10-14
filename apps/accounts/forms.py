"""
Forms and Formsets for the Accounts app.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from apps.accounts.models import BankAccount, Currency
from apps.core.validators import validate_iban


class OpenAccountForm(forms.ModelForm):
    """Form for opening a new bank account."""

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    account_type = forms.ChoiceField(
        choices=BankAccount.AccountType.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = BankAccount
        fields = ["currency", "account_type"]

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        currency = cleaned_data.get("currency")
        account_type = cleaned_data.get("account_type")
        if self.user and currency and account_type:
            exists = BankAccount.all_objects.filter(
                owner=self.user,
                currency=currency,
                account_type=account_type,
                is_deleted=False,
            ).exists()
            if exists:
                raise ValidationError(
                    f"You already have an active {account_type} account in {currency.code}."
                )
        return cleaned_data


class BeneficiaryForm(forms.Form):
    """Form for adding or editing a saved beneficiary."""

    nickname = forms.CharField(
        label="Contact Nickname / Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "e.g. John Doe, Rent Landlord",
                "required": "required",
            }
        ),
    )
    iban = forms.CharField(
        label="Recipient IBAN",
        max_length=34,
        validators=[validate_iban],
        widget=forms.TextInput(
            attrs={
                "class": "form-input font-mono",
                "placeholder": "KZ...",
                "required": "required",
            }
        ),
    )
    is_favorite = forms.BooleanField(
        label="Add to Favorites",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean_iban(self):
        iban = self.cleaned_data.get("iban", "").strip().upper()
        validate_iban(iban)
        # Check that destination account exists
        target = BankAccount.all_objects.filter(iban=iban, is_deleted=False).first()
        if not target:
            raise ValidationError("No active RocketBank account found with this IBAN.")
        self.target_account = target
        return iban


BeneficiaryFormSet = formset_factory(
    BeneficiaryForm,
    extra=2,
    can_delete=True,
)
