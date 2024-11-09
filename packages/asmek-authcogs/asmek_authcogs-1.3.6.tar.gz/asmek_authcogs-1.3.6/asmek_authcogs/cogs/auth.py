from aadiscordbot.app_settings import get_site_url
from discord.colour import Color
from discord.commands import SlashCommandGroup
from discord.embeds import Embed
from discord.ext import commands

from django.conf import settings

from allianceauth.eveonline.evelinks.eveimageserver import alliance_logo_url
from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    auth_commands = SlashCommandGroup(
        "auth", "Links for the Auth", guild_ids=[int(settings.DISCORD_GUILD_ID)]
    )

    # ASMEK Home
    @auth_commands.command(
        name="home",
        description="ASMEK Auth",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    async def home(self, ctx):
        """
        Returns a link to the Corp Auth Home
        """
        logger.info("test message")
        embed = Embed(title=settings.SITE_NAME + " Auth")
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.colour = Color.blurple()

        embed.description = (
            "All Authentication functions for "
            + settings.SITE_NAME
            + " are handled through our Auth."
        )

        url = get_site_url()

        embed.url = url

        return await ctx.respond(embed=embed)

    # ALLIANCE home
    @auth_commands.command(
        name="alliance",
        description="Alliance Auth",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    async def alliance(self, ctx):
        """
        Returns a link to the Alliance Auth Home
        """

        embed = Embed(title=settings.ASMEK_ALLIANCE_NAME + " Auth")

        embed.colour = Color.blurple()
        embed.set_thumbnail(url=alliance_logo_url(settings.ASMEK_ALLIANCE_ID, 256))

        embed.description = (
            "All Authentication functions for "
            + settings.ASMEK_ALLIANCE_NAME
            + " are handled through their Auth."
        )

        url = settings.ASMEK_ALLIANCE_URL

        embed.url = url

        return await ctx.respond(embed=embed)

    # corp wiki
    @auth_commands.command(
        name="wiki",
        description="Corp Wiki",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    async def wiki(self, ctx):
        """
        Returns a link to the Corp wiki page
        """

        embed = Embed(title="Corp Wiki")
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.colour = Color.blurple()

        embed.description = "The wiki contains important Alerts, helpful information, and corp and alliance policies."

        url = get_site_url() + "/wiki/"

        embed.url = url

        return await ctx.respond(embed=embed)

    # corp audit
    @auth_commands.command(
        name="audit",
        description="Character audit",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    async def audit(self, ctx):
        """
        Returns a link to the Corp character audit page
        """

        embed = Embed(title="Character Audit")
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.colour = Color.blurple()

        embed.description = "The character audit is what pulls in all the data for your characters. All characters owned by a member must be in this system."

        url = get_site_url() + "/audit/r/"

        embed.url = url

        return await ctx.respond(embed=embed)

    # corp fittings
    @auth_commands.command(
        name="fittings",
        description="Fittings and Doctrines",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    async def fittings(self, ctx):
        """
        Returns a link to the Corp fittings page
        """

        embed = Embed(title="Corp Fittings and Doctrines")
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.colour = Color.blurple()

        embed.description = "The fittings and doctrines page lists various PVP and PVE fits used by the corp"

        url = get_site_url() + "/fittings/"

        embed.url = url

        return await ctx.respond(embed=embed)

    # corp buyback
    @auth_commands.command(
        name="buyback",
        description="Corp Buyback",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    async def buyback(self, ctx):
        """
        Returns a link to the Corp buyback page
        """

        embed = Embed(title="Gravy Boat Buyback")
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.colour = Color.blurple()

        embed.description = (
            "For all you cheese curd, french fry, gravy, and poutine sales needs!"
        )

        url = get_site_url() + "/buybackprogram/"

        embed.url = url

        return await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Auth(bot))
