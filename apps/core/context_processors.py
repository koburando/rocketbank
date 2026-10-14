"""
Global context processors for RocketBank templates.
"""

from django.utils import timezone


def global_context(request):
    """
    Provides unread notifications count, active currencies,
    and user's theme preference to all templates.
    """
    unread_count = 0
    theme_preference = "SYSTEM"

    if hasattr(request, "user") and request.user.is_authenticated:
        try:
            from apps.notifications.models import Notification

            unread_count = Notification.objects.filter(
                user=request.user,
                is_read=False,
            ).count()
        except Exception:
            unread_count = 0

        profile = getattr(request.user, "profile", None)
        if profile and hasattr(profile, "preferred_theme"):
            theme_preference = profile.preferred_theme

    if theme_preference == "SYSTEM":
        theme_preference = request.COOKIES.get("theme", "SYSTEM")

    try:
        from apps.accounts.models import Currency

        active_currencies = list(Currency.objects.filter(is_active=True).order_by("code"))
    except Exception:
        active_currencies = []

    return {
        "unread_notifications_count": unread_count,
        "active_currencies": active_currencies,
        "user_theme_preference": theme_preference,
        "current_year": timezone.now().year,
        "site_name": "RocketBank",
        "site_domain": "rocketbank.company",
    }
