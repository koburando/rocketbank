"""
Core middleware for RocketBank.
"""

import logging
import time

from django.utils import timezone

logger = logging.getLogger("apps.middleware")


class RequestTimingAndLastVisitMiddleware:
    """
    Middleware that records execution timing for each request,
    adds an X-Request-Duration header, logs duration,
    and tracks user's last activity timestamp in session.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()

        # Update last activity in session for authenticated users
        if hasattr(request, "user") and request.user.is_authenticated:
            request.session["last_activity"] = timezone.now().isoformat()

        response = self.get_response(request)

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
