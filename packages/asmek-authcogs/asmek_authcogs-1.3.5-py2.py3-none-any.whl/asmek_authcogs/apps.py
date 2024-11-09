"""
Application config
"""

# Django
from django.apps import AppConfig

from . import __version__


class AsmekAuthCogConfig(AppConfig):
    name = "asmek_authcogs"
    label = "asmek_authcogs"
    verbose_name = f"Asmek Auth Cogs v{__version__}"
