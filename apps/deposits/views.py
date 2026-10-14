"""
Views for the Deposits app: Catalog, User Deposits, and Open Deposit flow.
"""

from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from apps.core.mixins import AjaxResponseMixin
from apps.deposits.forms import OpenDepositForm
from apps.deposits.models import DepositProduct, UserDeposit


class DepositProductListView(ListView):
    """
    Financial Marketplace: Term Deposits Catalog (Screen 2).
    """

    model = DepositProduct
    template_name = "deposits/catalog.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        qs = DepositProduct.objects.filter(is_active=True)
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(title__icontains=search.strip())

        sort = self.request.GET.get("sort")
        if sort == "rate":
            qs = qs.order_by("-interest_rate")
        elif sort == "term":
            qs = qs.order_by("term_months")
        else:
            qs = qs.order_by("-interest_rate")
        return qs


class DepositListView(LoginRequiredMixin, ListView):
    """
    Client's Active and Closed Deposits (Screen 10a).
    """

    model = UserDeposit
    template_name = "deposits/deposit_list.html"
    context_object_name = "deposits"

    def get_queryset(self):
        return (
            UserDeposit.objects.filter(user=self.request.user)
            .select_related("product", "account__currency")
            .order_by("-start_date")
        )


class OpenDepositCreateView(LoginRequiredMixin, AjaxResponseMixin, FormView):
    """
    Open Term Deposit View (Screen 10b).
    """

    template_name = "deposits/deposit_open.html"
    form_class = OpenDepositForm
    success_url = reverse_lazy("deposits:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        slug = self.request.GET.get("product")
        if slug:
            p = DepositProduct.objects.filter(slug=slug).first()
            if p:
                initial["product"] = p
        return initial

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        account = form.cleaned_data["account"]
        amount = form.cleaned_data["amount"]

        with transaction.atomic():
            # Lock account and debit amount
            account.balance -= amount
            account.save(update_fields=["balance", "updated_at"])

            start = date.today()
            end = start + relativedelta(months=product.term_months)

            deposit = UserDeposit.objects.create(
                user=self.request.user,
                account=account,
                product=product,
                amount=amount,
                accrued_interest=0,
                start_date=start,
                end_date=end,
                status=UserDeposit.DepositStatus.ACTIVE,
            )

        messages.success(
            self.request,
            f"Successfully opened {product.title} with an initial deposit of {amount:,.2f} KZT! "
            f"Maturity date: {deposit.end_date}. Interest rate: {product.interest_rate}% APR.",
        )
        return super().form_valid(form)
