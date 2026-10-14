"""
Forms for the Transactions app.
"""

from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from apps.accounts.models import BankAccount
from apps.core.validators import validate_iban
from apps.transactions.models import Transaction, TransactionCategory


class MoneyTransferForm(forms.ModelForm):
    """
    ModelForm for executing money transfers with strict single-field and
    cross-field balance, status, and currency validation.
    """

    sender_account = forms.ModelChoiceField(
        label="From Account",
        queryset=BankAccount.objects.none(),
        widget=forms.Select(attrs={"class": "form-select", "required": "required"}),
    )
    receiver_iban = forms.CharField(
        label="Recipient IBAN",
        max_length=34,
        validators=[validate_iban],
        widget=forms.TextInput(
            attrs={
                "class": "form-input font-mono",
                "placeholder": "KZ...",
                "required": "required",
                "autocomplete": "off",
                "list": "saved_beneficiaries_list",
            }
        ),
        help_text="Enter a 20-character Kazakhstan IBAN starting with KZ.",
    )
    amount = forms.DecimalField(
        label="Transfer Amount",
        max_digits=15,
        decimal_places=2,
        min_value=Decimal("1.00"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-input font-mono",
                "placeholder": "0.00",
                "step": "0.01",
                "min": "1.00",
                "required": "required",
            }
        ),
    )
    category = forms.ModelChoiceField(
        label="Spending Category",
        queryset=TransactionCategory.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    description = forms.CharField(
        label="Payment Reference / Note",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "e.g. Rent, Freelance invoice, Dinner",
                "maxlength": "250",
            }
        ),
    )

    class Meta:
        model = Transaction
        fields = ["sender_account", "amount", "category", "description"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["sender_account"].queryset = BankAccount.all_objects.filter(
                owner=user,
                is_deleted=False,
                status=BankAccount.AccountStatus.ACTIVE,
            ).select_related("currency")

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount <= 0:
            raise ValidationError("Transfer amount must be strictly greater than zero.")
        return amount

    def clean_receiver_iban(self):
        iban = self.cleaned_data.get("receiver_iban", "").strip().upper()
        validate_iban(iban)
        receiver = BankAccount.all_objects.filter(iban=iban, is_deleted=False).first()
        if not receiver:
            raise ValidationError("Recipient account with this IBAN does not exist in RocketBank.")
        if receiver.status != BankAccount.AccountStatus.ACTIVE:
            raise ValidationError("Recipient account is currently frozen or inactive.")
        self.receiver_account = receiver
        return iban

    def clean(self):
        cleaned_data = super().clean()
        sender = cleaned_data.get("sender_account")
        amount = cleaned_data.get("amount")
        receiver = getattr(self, "receiver_account", None)

        if sender and receiver and sender.id == receiver.id:
            raise ValidationError("Sender and recipient accounts cannot be the same account.")

        if sender and amount:
            if sender.balance < amount:
                bal = f"{sender.balance} {sender.currency.code}"
                raise ValidationError(
                    f"Insufficient funds: Your account balance is {bal}, "
                    f"which is less than the requested transfer amount of {amount}."
                )

        if sender and receiver:
            if sender.currency_id != receiver.currency_id:
                raise ValidationError(
                    f"Cross-currency mismatch: sender is in {sender.currency.code} "
                    f"while recipient is in {receiver.currency.code}. "
                    "Multi-currency conversion required."
                )

        return cleaned_data
