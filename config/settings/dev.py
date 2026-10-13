"""
Development settings for RocketBank.
"""

from .base import *  # noqa: F401, F403
from .base import env

# ──────────────────────────────────────────────
# Debug
# ──────────────────────────────────────────────
DEBUG = True

# ──────────────────────────────────────────────
# Hosts
# ──────────────────────────────────────────────
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "0.0.0.0"])

# ──────────────────────────────────────────────
# CSRF
# ──────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["http://localhost", "http://127.0.0.1"],
)

# ──────────────────────────────────────────────
# Email (console backend for development)
# ──────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
