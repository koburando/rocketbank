"""
Forms for the Deposits app.
"""

from django import forms
from django.core.exceptions import ValidationError

from apps.accounts.models import BankAccount
from apps.deposits.models import DepositProduct, UserDeposit


class OpenDepositForm(forms.ModelForm):
    """
    Form for opening a fixed-term deposit linked to a bank account.
    """

    product = forms.ModelChoiceField(
        label="Deposit Program",
        queryset=DepositProduct.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-select", "required": "required"}),
    )
    account = forms.ModelChoiceField(
        label="Fund from Account",
        queryset=BankAccount.objects.none(),
        widget=forms.Select(attrs={"class": "form-select", "required": "required"}),
    )
    amount = forms.DecimalField(
        label="Deposit Amount (KZT)",
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-input font-mono",
                "placeholder": "e.g. 500000",
                "step": "10000",
                "required": "required",
            }
        ),
    )

    class Meta:
        model = UserDeposit
        fields = ["product", "account", "amount"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["account"].queryset = BankAccount.all_objects.filter(
                owner=user,
                is_deleted=False,
                status=BankAccount.AccountStatus.ACTIVE,
            ).select_related("currency")

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        account = cleaned_data.get("account")
        amount = cleaned_data.get("amount")

        if product and amount:
            if amount < product.min_amount:
                raise ValidationError(
                    f"Minimum initial deposit for {product.title} is {product.min_amount:,.0f} KZT."
                )

        if account and amount:
            if account.balance < amount:
                bal = f"{account.balance:,.2f} {account.currency.code}"
                raise ValidationError(
                    f"Insufficient funds: Account balance is {bal}, "
                    f"which is less than {amount:,.2f} KZT."
                )

        return cleaned_data
