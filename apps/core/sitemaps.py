"""
Sitemaps configuration for RocketBank SEO.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.cards.models import CardProduct
from apps.credits.models import LoanProduct


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "about",
            "contacts",
            "support:faq",
            "cards:catalog",
            "credits:catalog",
            "deposits:catalog",
            "credits:calculator",
        ]

    def location(self, item):
        return reverse(item)


class CardProductSitemap(Sitemap):
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return CardProduct.objects.filter(is_active=True)

    def location(self, item):
        return reverse("cards:detail", kwargs={"slug": item.slug})


class CreditProductSitemap(Sitemap):
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return LoanProduct.objects.filter(is_active=True)

    def location(self, item):
        return reverse("credits:detail", kwargs={"slug": item.slug})


sitemaps = {
    "static": StaticViewSitemap,
    "cards": CardProductSitemap,
    "credits": CreditProductSitemap,
}
