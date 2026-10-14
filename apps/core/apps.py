from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Core"

    def ready(self):
        import sys

        from .converters import register_custom_converters

        register_custom_converters()

        # Python 3.14 compatibility patch for Django BaseContext.__copy__
        if sys.version_info >= (3, 14):
            from django.template.context import BaseContext

            def _patched_context_copy(ctx):
                duplicate = ctx.__class__.__new__(ctx.__class__)
                duplicate.__dict__.update(ctx.__dict__)
                duplicate.dicts = ctx.dicts[:]
                return duplicate

            BaseContext.__copy__ = _patched_context_copy
