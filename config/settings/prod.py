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
CSRF_TRUSTED_ORIGINS = [
    "http://rocketbank.company",
    "https://rocketbank.company",
    "http://www.rocketbank.company",
    "https://www.rocketbank.company",
    "http://4.240.88.237",
]

# ──────────────────────────────────────────────
# Security hardening
# ──────────────────────────────────────────────
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=False)
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)
# NOTE: Commented out until SSL/TLS is fully configured on the server.
# Once SSL is set up, uncomment this line to support HTTPS behind a reverse proxy.
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
