"""
Views for the Cards app: Marketplace Catalog, Detail with Reviews, Management,
3-Step Wizard Application, and Card Freeze Toggle FBV.
"""

import random
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, View

from apps.accounts.models import BankAccount
from apps.cards.forms import (
    CardWizardStep1Form,
    CardWizardStep2Form,
    CardWizardStep3Form,
)
from apps.cards.models import BankCard, CardProduct
from apps.support.models import FAQ


class CardProductListView(ListView):
    """
    Financial Marketplace: Cards Catalog (Screen 2).
    Search, filter by tier, sort, and pagination.
    """

    model = CardProduct
    template_name = "cards/catalog.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        qs = CardProduct.objects.filter(is_active=True)
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(title__icontains=search.strip())

        tier = self.request.GET.get("tier")
        if tier:
            qs = qs.filter(tier=tier)

        sort = self.request.GET.get("sort")
        if sort == "cashback":
            qs = qs.order_by("-cashback_percent")
        elif sort == "fee":
            qs = qs.order_by("annual_fee")
        else:
            qs = qs.order_by("tier")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tiers"] = CardProduct.CardTier.choices
        return context


class CardProductDetailView(DetailView):
    """
    Card Product Detail Page (Screen 3).
    Includes related card tiers, product specs, reviews, and JSON-LD schema.
    """

    model = CardProduct
    template_name = "cards/detail.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["related_products"] = CardProduct.objects.filter(
            is_active=True
        ).exclude(id=product.id)[:3]
        context["faqs"] = FAQ.objects.filter(
            is_published=True,
            category__icontains="card",
        )[:4]
        return context


class CardListView(LoginRequiredMixin, ListView):
    """
    Client's Cards Management Page (Screen 8a).
    """

    model = BankCard
    template_name = "cards/card_list.html"
    context_object_name = "cards"

    def get_queryset(self):
        return BankCard.objects.filter(
            account__owner=self.request.user,
            account__is_deleted=False,
        ).select_related("account__currency", "product").order_by("-issued_at")


class CardApplyWizardView(LoginRequiredMixin, View):
    """
    Multi-Step Card Application Wizard (Screen 8b & Section 2 Requirement).
    Step 1: Product & Tier Selection
    Step 2: Account Linking & Limit
    Step 3: Cardholder Name, Delivery & Final Confirmation
    """

    template_name = "cards/card_apply_wizard.html"

    def get_wizard_data(self):
        return self.request.session.get("card_wizard_data", {})

    def save_wizard_data(self, data):
        self.request.session["card_wizard_data"] = data
        self.request.session.modified = True

    def clear_wizard_data(self):
        self.request.session.pop("card_wizard_data", None)

    def get(self, request, *args, **kwargs):
        step = int(request.GET.get("step", 1))
        wizard_data = self.get_wizard_data()

        # Pre-select product if coming from catalog detail
        product_slug = request.GET.get("product")
        if product_slug and "product_id" not in wizard_data:
            prod = CardProduct.objects.filter(slug=product_slug).first()
            if prod:
                wizard_data["product_id"] = prod.id
                self.save_wizard_data(wizard_data)

        if step == 1:
            initial = {"product": wizard_data.get("product_id")}
            form = CardWizardStep1Form(initial=initial)
        elif step == 2:
            if not wizard_data.get("product_id"):
                return redirect(f"{reverse('cards:apply')}?step=1")
            initial = {
                "account": wizard_data.get("account_id"),
                "daily_limit": wizard_data.get("daily_limit", "500000.00"),
            }
            form = CardWizardStep2Form(initial=initial, user=request.user)
        elif step == 3:
            if not wizard_data.get("product_id") or not wizard_data.get("account_id"):
                return redirect(f"{reverse('cards:apply')}?step=1")
            address_initial = getattr(getattr(request.user, "profile", None), "address", "")
            initial = {
                "cardholder_name": wizard_data.get(
                    "cardholder_name",
                    f"{request.user.first_name} {request.user.last_name}".strip().upper()
                    or request.user.username.upper(),
                ),
                "delivery_address": wizard_data.get("delivery_address", address_initial),
            }
            form = CardWizardStep3Form(initial=initial)
        else:
            return redirect(f"{reverse('cards:apply')}?step=1")

        selected_product = None
        if wizard_data.get("product_id"):
            selected_product = CardProduct.objects.filter(id=wizard_data["product_id"]).first()

        selected_account = None
        if wizard_data.get("account_id"):
            selected_account = BankAccount.all_objects.filter(id=wizard_data["account_id"]).first()

        return render(
            request,
            self.template_name,
            {
                "step": step,
                "form": form,
                "selected_product": selected_product,
                "selected_account": selected_account,
                "wizard_data": wizard_data,
            },
        )

    def post(self, request, *args, **kwargs):
        step = int(request.GET.get("step", 1))
        wizard_data = self.get_wizard_data()

        if step == 1:
            form = CardWizardStep1Form(request.POST)
            if form.is_valid():
                wizard_data["product_id"] = form.cleaned_data["product"].id
                self.save_wizard_data(wizard_data)
                return redirect(f"{reverse('cards:apply')}?step=2")
        elif step == 2:
            form = CardWizardStep2Form(request.POST, user=request.user)
            if form.is_valid():
                wizard_data["account_id"] = str(form.cleaned_data["account"].id)
                wizard_data["daily_limit"] = str(form.cleaned_data["daily_limit"])
                self.save_wizard_data(wizard_data)
                return redirect(f"{reverse('cards:apply')}?step=3")
        elif step == 3:
            form = CardWizardStep3Form(request.POST)
            if form.is_valid():
                product_id = wizard_data.get("product_id")
                account_id = wizard_data.get("account_id")
                daily_limit = wizard_data.get("daily_limit", "500000.00")

                product = get_object_or_404(CardProduct, id=product_id)
                account = get_object_or_404(
                    BankAccount.all_objects,
                    id=account_id,
                    owner=request.user,
                )

                # Issue new Card
                with transaction.atomic():
                    # Generate masked card number: 4400 12** **** 1234
                    last4 = f"{random.randint(1000, 9999)}"
                    masked = f"4400 12** **** {last4}"
                    expiry = date.today() + relativedelta(years=3)

                    card = BankCard.objects.create(
                        account=account,
                        product=product,
                        card_number_masked=masked,
                        expiry_date=expiry,
                        daily_limit=daily_limit,
                        status=BankCard.CardStatus.ACTIVE,
                    )

                self.clear_wizard_data()
                delivery_preview = form.cleaned_data["delivery_address"][:40]
                messages.success(
                    request,
                    f"Congratulations! Your new {product.title} has been successfully issued! "
                    f"Card Number: {card.card_number_masked}. Delivery to {delivery_preview}...",
                )
                return redirect("cards:list")
        else:
            return redirect(f"{reverse('cards:apply')}?step=1")

        # Form is invalid
        selected_product = None
        if wizard_data.get("product_id"):
            selected_product = CardProduct.objects.filter(id=wizard_data["product_id"]).first()

        selected_account = None
        if wizard_data.get("account_id"):
            selected_account = BankAccount.all_objects.filter(id=wizard_data["account_id"]).first()

        return render(
            request,
            self.template_name,
            {
                "step": step,
                "form": form,
                "selected_product": selected_product,
                "selected_account": selected_account,
                "wizard_data": wizard_data,
            },
        )


@login_required
@require_POST
def toggle_card_freeze(request, pk):
    """
    Function-Based View (FBV) with explicit POST handling and decorators (Section 7).
    Quickly toggles card status between ACTIVE and BLOCKED.
    """
    card = get_object_or_404(
        BankCard.objects.select_related("account"),
        pk=pk,
        account__owner=request.user,
    )

    if card.status == BankCard.CardStatus.ACTIVE:
        card.transition_to(BankCard.CardStatus.BLOCKED)
        messages.warning(
            request,
            f"Card {card.card_number_masked} has been frozen. All outgoing transactions blocked.",
        )
    elif card.status == BankCard.CardStatus.BLOCKED:
        card.transition_to(BankCard.CardStatus.ACTIVE)
        messages.success(
            request,
            f"Card {card.card_number_masked} has been unfrozen and is now active.",
        )
    else:
        messages.error(
            request,
            f"Cannot toggle status for a card that is {card.get_status_display().lower()}.",
        )

    redirect_url = request.META.get("HTTP_REFERER") or reverse("cards:list")
    return redirect(redirect_url)
