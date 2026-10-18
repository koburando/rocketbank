"""
Django management command to compile PO files into MO binaries without gettext.
"""

from django.conf import settings
from django.core.management.base import BaseCommand

from scripts.compile_mo import compile_all


class Command(BaseCommand):
    help = "Pure-Python PO to MO compiler for RocketBank."

    def handle(self, *args, **options):
        self.stdout.write("Compiling PO translation catalogs to MO binaries...")
        compile_all(settings.BASE_DIR)
        self.stdout.write(self.style.SUCCESS("All MO catalogs compiled successfully."))
