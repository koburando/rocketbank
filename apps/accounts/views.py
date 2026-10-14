"""
Views for the Accounts app: Dashboard, Accounts List, Detail, and Beneficiaries Formset.
"""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
)

from apps.accounts.forms import BeneficiaryFormSet, OpenAccountForm
from apps.accounts.models import BankAccount, Beneficiary, SavedBeneficiary
from apps.accounts.selectors import get_balance_summary, get_user_accounts
from apps.accounts.services import create_bank_account
from apps.core.mixins import AjaxResponseMixin, OwnerRequiredMixin
from apps.transactions.selectors import get_account_transactions


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Client Dashboard (Screen 4).
    Displays portfolio balance, quick actions, accounts, and recent transactions.
    """

    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["summary"] = get_balance_summary(user)
        context["accounts"] = list(get_user_accounts(user))

        # Recent transactions across all user accounts
        from apps.transactions.models import Transaction

        user_account_ids = [a.id for a in context["accounts"]]
        context["recent_transactions"] = (
            Transaction.objects.filter(sender_account_id__in=user_account_ids)
            | Transaction.objects.filter(receiver_account_id__in=user_account_ids)
        ).select_related(
            "currency", "category", "sender_account", "receiver_account"
        ).order_by("-created_at")[:8]

        # Active saving goals
        from apps.analytics.models import SavingGoal

        context["saving_goals"] = SavingGoal.objects.filter(user=user)[:3]

        return context


class BankAccountListView(LoginRequiredMixin, ListView):
    """
    Accounts List View (Screen 5a).
    """

    model = BankAccount
    template_name = "accounts/account_list.html"
    context_object_name = "accounts"
    paginate_by = 10

    def get_queryset(self):
        qs = BankAccount.all_objects.filter(
            owner=self.request.user, is_deleted=False
        ).select_related("currency")
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(iban__icontains=search.strip())
        acc_type = self.request.GET.get("type")
        if acc_type:
            qs = qs.filter(account_type=acc_type)
        return qs.order_by("-opened_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary"] = get_balance_summary(self.request.user)
        return context


class BankAccountDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    """
    Account Detail Page (Screen 5b).
    Strict table markup with caption, thead, tbody, th scope="col".
    """

    model = BankAccount
    template_name = "accounts/account_detail.html"
    context_object_name = "account"
    owner_field = "owner"

    def get_queryset(self):
        return BankAccount.all_objects.filter(is_deleted=False).select_related("currency")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.object
        context["transactions"] = get_account_transactions(account, limit=30)
        context["cards"] = account.cards.select_related("product").all()
        return context


class AccountByIbanDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    """
    Account Detail View accessed via custom <iban:iban> path converter.
    """

    model = BankAccount
    template_name = "accounts/account_detail.html"
    context_object_name = "account"
    slug_field = "iban"
    slug_url_kwarg = "iban"
    owner_field = "owner"

    def get_queryset(self):
        return BankAccount.all_objects.filter(is_deleted=False).select_related("currency")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = get_account_transactions(self.object, limit=30)
        context["cards"] = self.object.cards.select_related("product").all()
        return context


class OpenAccountCreateView(LoginRequiredMixin, AjaxResponseMixin, FormView):
    """
    Form view for opening a new bank account.
    """

    template_name = "accounts/account_open.html"
    form_class = OpenAccountForm
    success_url = reverse_lazy("accounts:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        currency = form.cleaned_data["currency"]
        account_type = form.cleaned_data["account_type"]
        account = create_bank_account(
            owner=self.request.user,
            currency_code=currency.code,
            account_type=account_type,
            initial_balance=Decimal("0"),
        )
        acc_type_name = account.get_account_type_display()
        messages.success(
            self.request,
            f"Successfully opened a new {acc_type_name} account in {currency.code}! "
            f"Your IBAN: {account.iban}",
        )
        return super().form_valid(form)


class BeneficiaryFormsetView(LoginRequiredMixin, FormView):
    """
    Beneficiaries Management with Formset (Screen 12 & Section 2 Requirement).
    Allows managing multiple saved contacts at once.
    """

    template_name = "accounts/beneficiaries.html"
    form_class = BeneficiaryFormSet
    success_url = reverse_lazy("accounts:beneficiaries")

    def get_initial(self):
        saved = SavedBeneficiary.objects.filter(
            beneficiary__owner=self.request.user
        ).select_related("beneficiary__account")
        initial = []
        for s in saved:
            initial.append(
                {
                    "nickname": s.nickname,
                    "iban": s.beneficiary.account.iban,
                    "is_favorite": s.is_favorite,
                }
            )
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["existing_beneficiaries"] = SavedBeneficiary.objects.filter(
            beneficiary__owner=self.request.user
        ).select_related("beneficiary__account")
        return context

    @transaction.atomic
    def form_valid(self, formset):
        for form in formset:
            if not form.is_valid() or not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE"):
                # Handle delete
                iban = form.cleaned_data.get("iban")
                if iban:
                    SavedBeneficiary.objects.filter(
                        beneficiary__owner=self.request.user,
                        beneficiary__account__iban=iban,
                    ).delete()
                continue

            nickname = form.cleaned_data.get("nickname")
            iban = form.cleaned_data.get("iban")
            is_favorite = form.cleaned_data.get("is_favorite", False)

            if nickname and iban:
                target_account = getattr(form, "target_account", None)
                if not target_account:
                    target_account = BankAccount.all_objects.filter(iban=iban).first()

                if target_account:
                    ben, _ = Beneficiary.objects.get_or_create(
                        owner=self.request.user,
                        account=target_account,
                    )
                    SavedBeneficiary.objects.update_or_create(
                        beneficiary=ben,
                        defaults={"nickname": nickname, "is_favorite": is_favorite},
                    )

        messages.success(self.request, "Beneficiaries list has been successfully updated!")
        return redirect(self.get_success_url())


class BeneficiaryDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    """
    Delete a saved beneficiary (CBV DeleteView).
    """

    model = SavedBeneficiary
    success_url = reverse_lazy("accounts:beneficiaries")
    owner_field = "beneficiary__owner"

    def get_queryset(self):
        return SavedBeneficiary.objects.filter(beneficiary__owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Beneficiary removed from contacts.")
        return super().delete(request, *args, **kwargs)
