from aadiscordbot.cogs.utils.decorators import sender_has_perm
from discord.commands import SlashCommandGroup
from discord.ext import commands

from django.conf import settings

from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


class Siege(commands.Cog):
    """
    All siege me!
    """

    def __init__(self, bot):
        self.bot = bot

    siege_commands = SlashCommandGroup(
        "siege",
        "SIEGE COLOURS!",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )

    @siege_commands.command(name="green", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("asmek_authcogs.siege_control")
    async def green(self, ctx, *, msg=""):
        """
        All Clear
        """
        if len(msg) == 0:
            msg = "SIEGE GREEN - Crab on!"
        siege_channel = self.bot.get_channel(int(settings.ASMEK_SIEGE_CHANNEL))
        await siege_channel.purge()
        await siege_channel.send(
            " @here "
            + msg
            + "\nhttps://media.discordapp.net/attachments/478100446238474282/671250121178218496/Green_w_Excav.gif"
        )
        await siege_channel.edit(name="💸querious-status")
        return await ctx.respond("Siege status updated to GREEN", ephemeral=True)

    @siege_commands.command(name="amber", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("asmek_authcogs.siege_control")
    async def amber(self, ctx, *, msg=""):
        """
        Ratting caps should dock, rorqs max tank
        """
        if len(msg) == 0:
            msg = "SIEGE AMBER - Caps dock / Rorqs max tank!"
        siege_channel = self.bot.get_channel(int(settings.ASMEK_SIEGE_CHANNEL))
        await siege_channel.purge()
        await siege_channel.send(
            "@here "
            + msg
            + "\nhttps://media.discordapp.net/attachments/726469660916318218/829165923436331039/unknown.png"
        )
        await siege_channel.edit(name="🟠querious-status")
        return await ctx.respond("Siege status updated to AMBER", ephemeral=True)

    @siege_commands.command(name="red", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("asmek_authcogs.siege_control")
    async def red(self, ctx, *, msg=""):
        """
        Everyone should dock up
        """
        if len(msg) == 0:
            msg = "SIEGE RED - Delve is dangerous!"
        siege_channel = self.bot.get_channel(int(settings.ASMEK_SIEGE_CHANNEL))
        await siege_channel.purge()
        await siege_channel.send(
            "@here "
            + msg
            + "\nhttps://media.discordapp.net/attachments/478100446238474282/671250121345728542/Red_Final.gif"
        )
        await siege_channel.edit(name="🔴querious-status")
        return await ctx.respond("Siege status updated to RED", ephemeral=True)


def setup(bot):
    bot.add_cog(Siege(bot))
