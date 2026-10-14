"""
Views for the Transactions app: Money Transfer, History with Regrouping, and Printable Receipt.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, FormView, ListView

from apps.accounts.models import BankAccount, SavedBeneficiary
from apps.core.mixins import AjaxResponseMixin
from apps.transactions.forms import MoneyTransferForm
from apps.transactions.models import Transaction, TransactionCategory
from apps.transactions.services import execute_transfer


class MoneyTransferView(LoginRequiredMixin, AjaxResponseMixin, FormView):
    """
    Money Transfer Page (Screen 6).
    Executes atomic money transfers between accounts.
    """

    template_name = "transactions/transfer.html"
    form_class = MoneyTransferForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        from_id = self.request.GET.get("from_account")
        if from_id:
            initial["sender_account"] = from_id
        to_iban = self.request.GET.get("to_iban")
        if to_iban:
            initial["receiver_iban"] = to_iban
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Beneficiaries for datalist auto-completion
        context["saved_beneficiaries"] = SavedBeneficiary.objects.filter(
            beneficiary__owner=self.request.user
        ).select_related("beneficiary__account")
        return context

    def form_valid(self, form):
        sender = form.cleaned_data["sender_account"]
        receiver = form.receiver_account
        amount = form.cleaned_data["amount"]
        category = form.cleaned_data.get("category")
        description = form.cleaned_data.get("description", "")

        try:
            txn = execute_transfer(
                sender_account_id=sender.id,
                receiver_account_id=receiver.id,
                amount=amount,
                currency_code=sender.currency.code,
                description=description,
                category=category,
            )
            messages.success(
                self.request,
                f"Transfer of {amount} {sender.currency.code} to {receiver.iban} "
                f"completed successfully! Reference: {txn.reference_number}",
            )
            return redirect("transactions:receipt", reference_number=txn.reference_number)
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


class TransactionListView(LoginRequiredMixin, ListView):
    """
    Transaction History Page (Screen 7a).
    Supports category filtering, search, and date regrouping.
    """

    model = Transaction
    template_name = "transactions/transaction_list.html"
    context_object_name = "transactions"
    paginate_by = 15

    def get_queryset(self):
        user = self.request.user
        user_account_ids = BankAccount.all_objects.filter(
            owner=user, is_deleted=False
        ).values_list("id", flat=True)

        qs = (
            Transaction.objects.filter(
                Q(sender_account_id__in=user_account_ids)
                | Q(receiver_account_id__in=user_account_ids)
            )
            .select_related("currency", "category", "sender_account", "receiver_account")
            .order_by("-created_at")
        )

        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(
                Q(reference_number__icontains=search.strip())
                | Q(description__icontains=search.strip())
                | Q(sender_account__iban__icontains=search.strip())
                | Q(receiver_account__iban__icontains=search.strip())
            )

        cat = self.request.GET.get("category")
        if cat:
            qs = qs.filter(category__slug=cat)

        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = TransactionCategory.objects.all()
        return context


class TransactionDetailView(LoginRequiredMixin, DetailView):
    """
    Transaction Receipt Detail Page (Screen 7b).
    Accessed via custom <ref:reference_number> converter.
    Includes @media print styling and printable receipt statement.
    """

    model = Transaction
    template_name = "transactions/receipt.html"
    context_object_name = "transaction"

    def get_object(self, queryset=None):
        ref = self.kwargs.get("reference_number")
        txn = get_object_or_404(
            Transaction.objects.select_related(
                "sender_account__owner",
                "receiver_account__owner",
                "currency",
                "category",
            ),
            reference_number=ref,
        )
        user = self.request.user
        # Ensure user is either sender or receiver (or staff)
        is_sender = txn.sender_account and txn.sender_account.owner_id == user.id
        is_receiver = txn.receiver_account and txn.receiver_account.owner_id == user.id

        if not (is_sender or is_receiver or user.is_staff):
            raise PermissionDenied("You do not have permission to view this transaction receipt.")
        return txn
