"""App Settings"""

# Django
from django.conf import settings

# put your app settings here
ASMEK_AUTHCOGS_COGS = getattr(
    settings,
    "ASMEK_AUTHCOGS_COGS",
    [
        "asmek_authcogs.cogs.about",  # make sure to remove the about cog from aadiscordbot if using this
        "asmek_authcogs.cogs.auth",
        "asmek_authcogs.cogs.links",
        "asmek_authcogs.cogs.siege",
        "asmek_authcogs.cogs.hr",
    ],
)
