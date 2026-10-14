"""
Views for the Credits app: Catalog, Detail, User Loans, Loan Calculator, and Loan Application.
"""

from datetime import date
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from apps.core.mixins import AjaxResponseMixin
from apps.credits.forms import LoanApplicationForm, LoanCalculatorForm
from apps.credits.models import LoanApplication, LoanProduct, LoanSchedule


class CreditProductListView(ListView):
    """
    Financial Marketplace: Loans & Credits Catalog (Screen 2).
    """

    model = LoanProduct
    template_name = "credits/catalog.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        qs = LoanProduct.objects.filter(is_active=True)
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(title__icontains=search.strip())

        sort = self.request.GET.get("sort")
        if sort == "rate":
            qs = qs.order_by("interest_rate")
        elif sort == "amount":
            qs = qs.order_by("-max_amount")
        else:
            qs = qs.order_by("title")
        return qs


class CreditProductDetailView(DetailView):
    """
    Loan Product Detail Page (Screen 3).
    """

    model = LoanProduct
    template_name = "credits/detail.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["related_products"] = (
            LoanProduct.objects.filter(is_active=True).exclude(id=product.id)[:3]
        )
        return context


class LoanListView(LoginRequiredMixin, ListView):
    """
    User's Loans & Credit Applications (Screen 9a).
    """

    model = LoanApplication
    template_name = "credits/loan_list.html"
    context_object_name = "loans"

    def get_queryset(self):
        return (
            LoanApplication.objects.filter(user=self.request.user)
            .select_related("product")
            .prefetch_related("schedule_entries")
            .order_by("-created_at")
        )


class LoanCalculatorView(FormView):
    """
    Interactive Loan Calculator (Screen 9b).
    Calculates annuity monthly payments and generates amortization schedule.
    """

    template_name = "credits/loan_calculator.html"
    form_class = LoanCalculatorForm

    def get_initial(self):
        initial = super().get_initial()
        slug = self.request.GET.get("product")
        if slug:
            p = LoanProduct.objects.filter(slug=slug).first()
            if p:
                initial["product"] = p
        return initial

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        amount = form.cleaned_data["amount"]
        term_months = form.cleaned_data["term_months"]

        # Calculate Annuity Monthly Payment:
        # r = annual_rate / 12 / 100
        # PMT = P * [r * (1 + r)^n] / [(1 + r)^n - 1]
        rate_monthly = (product.interest_rate / Decimal("100")) / Decimal("12")

        if rate_monthly > 0:
            growth = (1 + rate_monthly) ** term_months
            monthly_payment = amount * ((rate_monthly * growth) / (growth - 1))
        else:
            monthly_payment = amount / Decimal(term_months)

        total_payment = monthly_payment * Decimal(term_months)
        total_interest = total_payment - amount

        # Build simulated amortization schedule
        schedule = []
        remaining_balance = amount
        start = date.today()

        for i in range(1, term_months + 1):
            interest_part = remaining_balance * rate_monthly
            principal_part = monthly_payment - interest_part
            remaining_balance = max(Decimal("0.00"), remaining_balance - principal_part)
            due = start + relativedelta(months=i)
            schedule.append(
                {
                    "installment": i,
                    "due_date": due,
                    "monthly_payment": monthly_payment,
                    "principal": principal_part,
                    "interest": interest_part,
                    "remaining": remaining_balance,
                }
            )

        context = self.get_context_data(
            form=form,
            calculated=True,
            product=product,
            amount=amount,
            term_months=term_months,
            monthly_payment=monthly_payment,
            total_payment=total_payment,
            total_interest=total_interest,
            schedule=schedule[:12],  # Preview first 12 installments
            schedule_count=len(schedule),
        )
        return self.render_to_response(context)


class LoanApplyCreateView(LoginRequiredMixin, AjaxResponseMixin, CreateView):
    """
    Loan Application Form View (Screen 9c & Section 5).
    """

    model = LoanApplication
    form_class = LoanApplicationForm
    template_name = "credits/loan_apply.html"
    success_url = reverse_lazy("credits:list")

    def get_initial(self):
        initial = super().get_initial()
        slug = self.request.GET.get("product")
        if slug:
            p = LoanProduct.objects.filter(slug=slug).first()
            if p:
                initial["product"] = p
        amount = self.request.GET.get("amount")
        if amount:
            initial["requested_amount"] = amount
        term = self.request.GET.get("term")
        if term:
            initial["term_months"] = term
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = LoanApplication.LoanStatus.SUBMITTED
        response = super().form_valid(form)

        # Generate tentative loan schedule entries
        loan = self.object
        product = loan.product
        rate_monthly = (product.interest_rate / Decimal("100")) / Decimal("12")
        growth = (1 + rate_monthly) ** loan.term_months
        monthly_payment = loan.requested_amount * ((rate_monthly * growth) / (growth - 1))
        remaining = loan.requested_amount

        for i in range(1, loan.term_months + 1):
            interest_part = remaining * rate_monthly
            principal_part = monthly_payment - interest_part
            remaining = max(Decimal("0.00"), remaining - principal_part)
            LoanSchedule.objects.create(
                loan=loan,
                installment_number=i,
                due_date=date.today() + relativedelta(months=i),
                principal_amount=principal_part,
                interest_amount=interest_part,
                is_paid=False,
            )

        messages.success(
            self.request,
            f"Loan Application #{loan.id} for {loan.requested_amount:,.2f} KZT submitted! "
            "Our automated scoring system is processing your approval.",
        )
        return response
