"""
Custom template tags and filters for RocketBank.
"""

from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter(name="mask_iban")
def mask_iban(value: str) -> str:
    """
    Mask an IBAN string leaving first 4 and last 4 characters visible.
    Example: 'KZ1234567890123456' -> 'KZ12 •••• •••• 3456'
    """
    if not value or not isinstance(value, str):
        return ""
    clean_val = value.replace(" ", "")
    if len(clean_val) < 8:
        return value

    prefix = clean_val[:4]
    suffix = clean_val[-4:]
    return f"{prefix} •••• •••• {suffix}"


@register.filter(name="currency_format")
def currency_format(value, currency_symbol=None) -> str:
    """
    Format a numeric amount with thousands separator and decimal places.
    Example: 1250000.5 -> '1,250,000.50 ₸'
    """
    if value is None or value == "":
        return "0.00"
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return str(value)

    formatted = f"{dec:,.2f}"
    if currency_symbol:
        symbols = {"KZT": "₸", "USD": "$", "EUR": "€", "RUB": "₽", "GBP": "£"}
        sym = symbols.get(str(currency_symbol).upper(), str(currency_symbol))
        return f"{formatted} {sym}"
    return formatted


@register.filter(name="status_badge_class")
def status_badge_class(status: str) -> str:
    """
    Map domain status choices to CSS badge variant classes.
    """
    if not status:
        return "badge--secondary"

    key = str(status).upper()
    mapping = {
        # Positive / Success
        "ACTIVE": "badge--success",
        "COMPLETED": "badge--success",
        "VERIFIED": "badge--success",
        "APPROVED": "badge--success",
        "DISBURSED": "badge--success",
        "RESOLVED": "badge--success",
        "SUCCESS": "badge--success",
        # In-Progress / Warning
        "PENDING": "badge--warning",
        "SUBMITTED": "badge--warning",
        "UNDER_REVIEW": "badge--warning",
        "WAITING": "badge--warning",
        "IN_PROGRESS": "badge--warning",
        "WARNING": "badge--warning",
        # Negative / Danger
        "FROZEN": "badge--danger",
        "BLOCKED": "badge--danger",
        "REJECTED": "badge--danger",
        "FAILED": "badge--danger",
        "ERROR": "badge--danger",
        "URGENT": "badge--danger",
        # Inactive / Muted
        "CLOSED": "badge--muted",
        "CANCELLED": "badge--muted",
        "EXPIRED": "badge--muted",
        "EARLY_CLOSED": "badge--muted",
        "DRAFT": "badge--muted",
        "INFO": "badge--info",
        "LOW": "badge--muted",
        "MEDIUM": "badge--info",
        "HIGH": "badge--warning",
    }
    return mapping.get(key, "badge--secondary")


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs) -> str:
    """
    Update or append GET parameters for pagination, sorting, or filtering.
    Usage: href="?{% query_transform page=page_obj.next_page_number %}"
    """
    request = context.get("request")
    if not request:
        return ""

    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None and value != "":
            updated[key] = value
        else:
            updated.pop(key, None)

    return updated.urlencode()


@register.inclusion_tag("includes/quick_balance_widget.html", takes_context=True)
def quick_balance_widget(context):
    """
    Inclusion tag to render the user's quick balance card widget.
    """
    request = context.get("request")
    user = getattr(request, "user", None)
    summary = {
        "total_balance": Decimal("0"),
        "account_count": 0,
        "checking_balance": Decimal("0"),
        "savings_balance": Decimal("0"),
    }
    accounts = []

    if user and user.is_authenticated:
        try:
            from apps.accounts.selectors import get_balance_summary, get_user_accounts

            summary = get_balance_summary(user)
            accounts = list(get_user_accounts(user)[:3])
        except Exception:
            pass

    return {
        "summary": summary,
        "accounts": accounts,
        "user": user,
    }


@register.simple_tag(takes_context=True, name="tr")
def tr_tag(context, text: str) -> str:
    """
    Template tag to translate string using active request language:
    {% tr "Cards" %} -> "Карты" (if ru) or "Карталар" (if kk) or "Cards" (if en).
    """
    from apps.core.translations import t

    request = context.get("request")
    lang = getattr(request, "LANGUAGE_CODE", None) if request else None
    return t(text, lang=lang)


@register.simple_tag(takes_context=True, name="t")
def t_tag(context, text: str) -> str:
    """Shortcut alias for {% tr %}."""
    return tr_tag(context, text)

