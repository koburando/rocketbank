"""
URL configuration for RocketBank project.
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path


def health_check(request):
    """Health check endpoint for monitoring and load balancers."""
    return JsonResponse({"status": "ok", "service": "RocketBank"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health-check"),
]

# ── Admin site branding ──────────────────────────
admin.site.site_header = "RocketBank Core Admin"
admin.site.site_title = "RocketBank Admin"
admin.site.index_title = "Administration Dashboard"
