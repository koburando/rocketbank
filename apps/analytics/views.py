"""
Views for the Analytics app: Portfolio Breakdown, Saving Goals,
and HTML5 <meter>/<progress> visualizations.
"""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView

from apps.accounts.models import BankAccount
from apps.accounts.selectors import get_balance_summary
from apps.analytics.forms import SavingGoalForm
from apps.analytics.models import SavingGoal
from apps.core.mixins import OwnerRequiredMixin
from apps.transactions.models import Transaction
from apps.transactions.selectors import get_spending_by_category


class AnalyticsDashboardView(LoginRequiredMixin, FormView):
    """
    Analytics & Saving Goals Page (Screen 11).
    Visualizes spending, budget thresholds using <meter>, and goal targets using <progress>.
    """

    template_name = "analytics/dashboard.html"
    form_class = SavingGoalForm
    success_url = reverse_lazy("analytics:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        goals = SavingGoal.objects.filter(user=user).order_by("-created_at")
        context["goals"] = goals

        # Aggregate total saved vs total target
        total_target = goals.aggregate(s=Sum("target_amount"))["s"] or Decimal("0")
        total_saved = goals.aggregate(s=Sum("current_amount"))["s"] or Decimal("0")
        overall_progress = (total_saved / total_target * 100) if total_target > 0 else 0

        context["total_target"] = total_target
        context["total_saved"] = total_saved
        context["overall_progress"] = min(overall_progress, 100)

        # Spending Breakdown by Category
        user_accounts = BankAccount.all_objects.filter(owner=user, is_deleted=False)
        primary_account = user_accounts.first()
        if primary_account:
            context["category_spending"] = list(get_spending_by_category(primary_account)[:6])
        else:
            context["category_spending"] = []

        # Monthly Budget Health Meter calculation (Spend vs Income ratio)
        monthly_income = Decimal("750000.00")
        total_spent_this_month = Transaction.objects.filter(
            sender_account__owner=user,
            status=Transaction.TransactionStatus.COMPLETED,
        ).aggregate(s=Sum("amount"))["s"] or Decimal("0")

        context["budget_spent"] = total_spent_this_month
        context["budget_limit"] = monthly_income
        ratio = min((total_spent_this_month / monthly_income), Decimal("1.0"))
        context["budget_ratio"] = float(ratio)

        context["summary"] = get_balance_summary(user)
        return context

    def form_valid(self, form):
        goal = form.save(commit=False)
        goal.user = self.request.user
        goal.save()
        messages.success(
            self.request,
            f"Saving goal '{goal.title}' for {goal.target_amount:,.2f} KZT has been created!",
        )
        return redirect(self.get_success_url())


class SavingGoalDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    """
    Delete a saving goal (CBV DeleteView).
    """

    model = SavingGoal
    success_url = reverse_lazy("analytics:dashboard")
    owner_field = "user"

    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Saving goal deleted.")
        return super().delete(request, *args, **kwargs)
