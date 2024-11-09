import asyncio
import re

import discord
from discord import AutocompleteContext, option
from discord.commands import SlashCommandGroup
from discord.ext import commands
from securegroups.tasks import run_smart_groups

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from allianceauth.eveonline.models import EveCharacter
from allianceauth.eveonline.tasks import update_character
from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


# Validation Checks - These values must be defined in server settings
if not hasattr(settings, "ASMEK_RECRUIT_CHANNEL"):
    raise ValueError("ASMEK_RECRUIT_CHANNEL is not defined.")
if not hasattr(settings, "ASMEK_CORP_ROLEID"):
    raise ValueError("ASMEK_CORP_ROLEID is not defined.")
if not hasattr(settings, "ASMEK_HR_ROLEID"):
    raise ValueError("ASMEK_HR_ROLEID is not defined.")
if not hasattr(settings, "ASMEK_RECRUIT_MSG_1"):
    raise ValueError("ASMEK_RECRUIT_MSG_1 is not defined.")


# Returns the count of how many ASMEK_RECRUIT_MSG_# settings variables are available, assuming ASMEK_RECRUIT_MSG_1 will always exist
async def msgcount():
    i = 0
    while hasattr(settings, "ASMEK_RECRUIT_MSG_" + str(i + 1)):
        i += 1
    return i


# Returns whether the reaction clicked on by a user in recruitment is valid
async def valid_reaction(self, reaction, user):
    logger.info("valid reaction check")
    if reaction.message.channel.name == "RCT-" + user.name:
        if reaction.emoji == "\N{White Heavy Check Mark}":
            async for user in reaction.users():
                if user.id == self.bot.user.id:
                    logger.info("reaction is valid!")
                    return True
    logger.info("reaction is invalid")
    return False


class HR(commands.Cog):
    """
    Creates private thread for recruits.
    """

    def __init__(self, bot):
        self.bot = bot

    hr_commands = SlashCommandGroup(
        "hr",
        "Human Resources Commands",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )

    # Listener for added reactions to see whether additional recruitment messages should be sent
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if await valid_reaction(self, reaction, user):
            logger.info("Valid reaction detected")

            # Retrieve and normalize message content
            msg = re.sub("<.*?>", "{}", reaction.message.content).strip().lower()
            logger.info(f"Normalized message from reaction: {msg}")

            msgnum = await msgcount()

            for x in range(1, msgnum):
                msg_value = getattr(settings, f"ASMEK_RECRUIT_MSG_{x}", None)
                if msg_value:
                    # Normalize msg_value for comparison
                    normalized_msg_value = msg_value.strip().lower()
                    logger.info(
                        f"Checking against msg_value for x={x}: {normalized_msg_value}"
                    )

                    if msg == normalized_msg_value:
                        await reaction.message.clear_reactions()
                        logger.info("Message matched, reactions cleared")

                        next_msg = getattr(settings, f"ASMEK_RECRUIT_MSG_{x + 1}", None)
                        if next_msg:
                            messageinfo = await self.bot.get_channel(
                                reaction.message.channel.id
                            ).send(next_msg)
                            logger.info("Next message sent")

                            # Only add the reaction if x is less than the last message number
                            if x < (msgnum - 1):
                                await messageinfo.add_reaction(
                                    "\N{White Heavy Check Mark}"
                                )
                                logger.info("Reaction added to the next message")
                        else:
                            logger.info("No next message found, ending loop")
                        return
            logger.info("No match found for the current message")

    # Checks to see whether a thread exists for the given user and returns the thread ID if so
    async def thread_exist(self, member):
        chan = self.bot.get_channel(int(settings.ASMEK_RECRUIT_CHANNEL))
        for thread in chan.threads:
            if thread.name == "RCT-" + member.name:
                return thread.id
        return 0

    # Checks to see if target user is already in asmek
    async def target_in_corp(self, member):
        for userrole in member.roles:
            if userrole.id == int(settings.ASMEK_CORP_ROLEID):
                return True
        return False

    # Runs through the various check methods to determine whether a given recruitment invocation is valid
    async def can_recruit(self, ctx, member):
        threadid = await self.thread_exist(member)
        if await self.target_in_corp(member):
            await ctx.respond(
                "That user is already in the corporation.", ephemeral=True
            )
            return False
        elif threadid > 0:
            await ctx.respond(
                "That user already has an active recruitment thread: <#"
                + str(threadid)
                + ">",
                ephemeral=True,
            )
            return False
        return True

    # Sets up right-click user command for EVE recruitment
    @commands.user_command(
        name="Recruit to corp", guild_ids=[int(settings.DISCORD_GUILD_ID)]
    )
    @commands.has_role(int(settings.ASMEK_HR_ROLEID))
    async def recruit_user(self, ctx, member: discord.Member):
        if await self.can_recruit(ctx, member):
            channel = self.bot.get_channel(int(settings.ASMEK_RECRUIT_CHANNEL))
            threadname = "RCT-" + member.name
            recruitrole = ctx.guild.get_role(int(settings.ASMEK_HR_ROLEID))
            messagetext = settings.ASMEK_RECRUIT_MSG_1.format(
                member.mention, recruitrole.mention
            )
            threadinfo = await channel.create_thread(
                name=threadname,
                auto_archive_duration=10080,
                type=discord.ChannelType.private_thread,
            )
            messageinfo = await self.bot.get_channel(threadinfo.id).send(messagetext)
            if await msgcount() > 1:
                await messageinfo.add_reaction("\N{White Heavy Check Mark}")
            if int(settings.ASMEK_HR_ROLEID) in ctx.author.roles:
                await ctx.respond(
                    "Recruitment thread created: " + threadinfo.mention, ephemeral=True
                )
            else:
                await ctx.respond("Recruitment thread created!", ephemeral=True)

    # slash command to recruit
    @hr_commands.command(
        name="recruit",
        description="Recruit for EVE. Use an @ mention to choose the user.",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    @commands.has_role(int(settings.ASMEK_HR_ROLEID))
    async def recruit(self, ctx, member: discord.Member):
        if await self.can_recruit(ctx, member):
            channel = self.bot.get_channel(int(settings.ASMEK_RECRUIT_CHANNEL))
            threadname = "RCT-" + member.name
            recruitrole = ctx.guild.get_role(int(settings.ASMEK_HR_ROLEID))
            messagetext = settings.ASMEK_RECRUIT_MSG_1.format(
                member.mention, recruitrole.mention
            )
            threadinfo = await channel.create_thread(
                name=threadname,
                auto_archive_duration=10080,
                type=discord.ChannelType.private_thread,
            )

            messageinfo = await self.bot.get_channel(threadinfo.id).send(messagetext)
            if await msgcount() > 1:
                await messageinfo.add_reaction("\N{White Heavy Check Mark}")
            if int(settings.ASMEK_HR_ROLEID) in ctx.author.roles:
                await ctx.respond(
                    "Recruitment thread created: " + threadinfo.mention, ephemeral=True
                )
            else:
                await ctx.respond("Recruitment thread created!", ephemeral=True)

    # slash command for user to start own application
    @commands.slash_command(
        name="apply",
        description="Apply to corp",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    async def apply(self, ctx):
        mem = ctx.author
        if await self.can_recruit(ctx, mem):
            channel = self.bot.get_channel(int(settings.ASMEK_RECRUIT_CHANNEL))
            threadname = "RCT-" + ctx.author.name
            recruitrole = ctx.guild.get_role(int(settings.ASMEK_HR_ROLEID))
            messagetext = settings.ASMEK_RECRUIT_MSG_1.format(
                ctx.author.mention, recruitrole.mention
            )
            threadinfo = await channel.create_thread(
                name=threadname,
                auto_archive_duration=10080,
                type=discord.ChannelType.private_thread,
            )
            messageinfo = await self.bot.get_channel(threadinfo.id).send(messagetext)
            if await msgcount() > 1:
                await messageinfo.add_reaction("\N{White Heavy Check Mark}")
            if int(settings.ASMEK_HR_ROLEID) in ctx.author.roles:
                await ctx.respond(
                    "Recruitment thread created: " + threadinfo.mention, ephemeral=True
                )
            else:
                await ctx.respond("Recruitment thread created!", ephemeral=True)

    async def search_characters(ctx: AutocompleteContext):
        """Returns a list of colors that begin with the characters entered so far."""
        return list(
            EveCharacter.objects.filter(
                character_name__icontains=ctx.value
            ).values_list("character_name", flat=True)[:10]
        )

    # Sets up slash command for syncing all data of user
    @hr_commands.command(
        name="update_user",
        description="updates user",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    @commands.has_role(int(settings.ASMEK_HR_ROLEID))
    @option(
        "character",
        description="Search for a Character!",
        autocomplete=search_characters,
    )
    async def update_user(self, ctx, character: str):
        """
        Queue Update tasks for the character and all alts. Run compliant group
        """
        try:
            char = EveCharacter.objects.get(character_name=character)
            alts = (
                char.character_ownership.user.character_ownerships.all()
                .select_related("character")
                .values_list("character__character_id", flat=True)
            )
            for c in alts:
                update_character.delay(c)
            await ctx.respond(
                f"Sent tasks to update **{character}**'s Alts", ephemeral=True
            )
        except EveCharacter.DoesNotExist:
            return await ctx.respond(
                f"Character **{character}** does not exist in our Auth system",
                ephemeral=True,
            )
        except ObjectDoesNotExist:
            return await ctx.respond(
                f"**{character}** is Unlinked unable to update characters",
                ephemeral=True,
            )

        await asyncio.sleep(30)
        try:
            run_smart_groups()
            return await ctx.respond(
                "Sent task to update secure groups", ephemeral=True
            )
        except Exception:
            return await ctx.respond("secure group update failed", ephemeral=True)


def setup(bot):
    bot.add_cog(HR(bot))
