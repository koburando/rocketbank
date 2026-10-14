"""
URL configuration for RocketBank project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import JsonResponse
from django.urls import include, path

from apps.core.converters import register_custom_converters
from apps.core.sitemaps import sitemaps
from apps.core.views import AboutView, ContactsView, LandingHomeView, RobotsTxtView

# Ensure custom converters are registered
register_custom_converters()


def health_check(request):
    """Health check endpoint for monitoring and load balancers."""
    return JsonResponse({"status": "ok", "service": "RocketBank"})


urlpatterns = [
    # ── Admin & Monitoring ──────────────────────────
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health-check"),

    # ── SEO & Robots ────────────────────────────────
    path("robots.txt", RobotsTxtView.as_view(), name="robots-txt"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),

    # ── Public Pages ────────────────────────────────
    path("", LandingHomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contacts/", ContactsView.as_view(), name="contacts"),

    # ── Domain App URL Namespaces ───────────────────
    path("users/", include("apps.users.urls", namespace="users")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("cards/", include("apps.cards.urls", namespace="cards")),
    path("transactions/", include("apps.transactions.urls", namespace="transactions")),
    path("credits/", include("apps.credits.urls", namespace="credits")),
    path("deposits/", include("apps.deposits.urls", namespace="deposits")),
    path("analytics/", include("apps.analytics.urls", namespace="analytics")),
    path("notifications/", include("apps.notifications.urls", namespace="notifications")),
    path("support/", include("apps.support.urls", namespace="support")),
]

# Static & Media routing in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ── Admin site branding ──────────────────────────
admin.site.site_header = "RocketBank Core Admin"
admin.site.site_title = "RocketBank Admin"
admin.site.index_title = "Administration Dashboard"
