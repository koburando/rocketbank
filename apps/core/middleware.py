"""
Core middleware for RocketBank.
"""

import logging
import time

from django.conf import settings
from django.utils import timezone
from django.utils.translation import activate

logger = logging.getLogger("apps.middleware")


class RequestTimingAndLastVisitMiddleware:
    """
    Middleware that:
    1. Reads active language from cookie or session (defaulting to 'ru') and activates it.
    2. Records execution timing for each request and adds X-Request-Duration header.
    3. Tracks user's last activity timestamp in session.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Enforce active language preference (RU default, KK, EN)
        cookie_name = getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language")
        lang = request.COOKIES.get(cookie_name)
        if not lang and hasattr(request, "session"):
            lang = request.session.get("django_language") or request.session.get(cookie_name)

        if not lang and hasattr(request, "user") and request.user.is_authenticated:
            profile = getattr(request.user, "profile", None)
            if profile and getattr(profile, "preferred_language", None):
                lang = profile.preferred_language.lower()

        if lang not in ("ru", "kk", "en"):
            lang = "ru"

        activate(lang)
        request.LANGUAGE_CODE = lang

        start_time = time.perf_counter()

        # Update last activity in session for authenticated users
        if hasattr(request, "user") and request.user.is_authenticated:
            request.session["last_activity"] = timezone.now().isoformat()

        response = self.get_response(request)

        # Ensure language cookie is always set for client predictability
        if cookie_name not in request.COOKIES and cookie_name not in response.cookies:
            response.set_cookie(cookie_name, lang, max_age=31536000, path="/", samesite="Lax")

        duration = time.perf_counter() - start_time
        duration_str = f"{duration:.4f}s"
        response["X-Request-Duration"] = duration_str
        response["X-Request-Duration-Ms"] = f"{duration * 1000:.2f}ms"

        logger.info(
            "Path: %s | Method: %s | Status: %s | Duration: %s",
            request.path,
            request.method,
            getattr(response, "status_code", "-"),
            duration_str,
        )

        return response
