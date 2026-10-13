"""
Production settings for RocketBank.
"""

from .base import *  # noqa: F401, F403
from .base import env

# ──────────────────────────────────────────────
# Debug — MUST be False in production
# ──────────────────────────────────────────────
DEBUG = False

# ──────────────────────────────────────────────
# Hosts — strictly from environment
# ──────────────────────────────────────────────
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# ──────────────────────────────────────────────
# Security hardening
# ──────────────────────────────────────────────
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
