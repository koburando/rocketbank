"""
General public views: Landing Home, About RocketBank, Contacts,
Language Switcher, and SEO endpoints.
"""

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import activate
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


def switch_language(request, lang_code):
    """
    Switches active language cleanly via GET or POST, persists it in session & cookie,
    and safely redirects to HTTP_REFERER or '/'.
    """
    lang_code = (lang_code or "").lower().strip()
    if lang_code not in ("ru", "kk", "en"):
        lang_code = "ru"

    activate(lang_code)

    referer = request.META.get("HTTP_REFERER") or "/"
    if not url_has_allowed_host_and_scheme(url=referer, allowed_hosts={request.get_host()}):
        referer = "/"

    response = HttpResponseRedirect(referer)

    cookie_name = getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language")

    # Persist in session
    if hasattr(request, "session"):
        request.session[cookie_name] = lang_code
        request.session["django_language"] = lang_code

    # Persist in user profile if authenticated
    if hasattr(request, "user") and request.user.is_authenticated:
        profile = getattr(request.user, "profile", None)
        if profile and hasattr(profile, "preferred_language"):
            try:
                profile.preferred_language = lang_code.upper()
                profile.save(update_fields=["preferred_language"])
            except Exception:
                pass

    # Persist in cookie (1 year)
    response.set_cookie(
        cookie_name,
        lang_code,
        max_age=31536000,
        path="/",
        samesite="Lax",
    )
    return response


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
