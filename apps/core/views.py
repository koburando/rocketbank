"""
General public views: Landing Home, About RocketBank, Contacts, and SEO endpoints.
"""

from django.http import HttpResponse
from django.views.generic import TemplateView, View

from apps.accounts.models import Currency
from apps.cards.models import CardProduct
from apps.credits.models import LoanProduct
from apps.deposits.models import DepositProduct


class LandingHomeView(TemplateView):
    """
    Landing Home Page (Screen 1).
    Rich introduction to RocketBank, featured products, exchange rates, and stats.
    """

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_cards"] = CardProduct.objects.filter(is_active=True)[:3]
        context["featured_loans"] = LoanProduct.objects.filter(is_active=True)[:3]
        context["featured_deposits"] = DepositProduct.objects.filter(is_active=True)[:3]
        context["currencies"] = Currency.objects.filter(is_active=True).order_by("code")
        return context


class AboutView(TemplateView):
    """
    About RocketBank Page (Screen 18).
    Includes architectural highlights, executive team with <figure>/<figcaption>,
    <picture>/<source srcset>, loading="lazy", and embedded video/map.
    """

    template_name = "about.html"


class ContactsView(TemplateView):
    """
    Contacts & Branches Page (Screen 19).
    """

    template_name = "contacts.html"


class RobotsTxtView(View):
    """
    Serves robots.txt dynamically with sitemap reference.
    """

    def get(self, request):
        content = (
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /admin/\n"
            "Disallow: /accounts/\n"
            "Disallow: /transactions/\n"
            "Disallow: /notifications/\n"
            "Disallow: /users/\n\n"
            f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml\n"
        )
        return HttpResponse(content, content_type="text/plain")


class OfflineView(TemplateView):
    """
    PWA Offline Fallback Page (Section 10 & 15).
    """

    template_name = "offline.html"
