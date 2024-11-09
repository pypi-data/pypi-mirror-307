from aadiscordbot.cogs.utils.decorators import sender_has_perm
from discord import AutocompleteContext, Embed, InputTextStyle, Interaction, option
from discord.colour import Color
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord.ui import InputText, Modal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from allianceauth.services.hooks import get_extension_logger

from asmek_authcogs.models import Link

logger = get_extension_logger(__name__)


class Links(commands.Cog):
    """
    Helpful links
    """

    def __init__(self, bot):
        self.bot = bot

    links_commands = SlashCommandGroup(
        "links",
        "Useful links to sites or programs",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )

    async def search_links(ctx: AutocompleteContext):
        """Returns a list of links that begin with the characters entered so far."""
        return list(
            Link.objects.filter(name__icontains=ctx.value).values_list(
                "name", flat=True
            )[:10]
        )

    class AddModal(Modal):
        def __init__(self):
            super().__init__(title="Add a link")

            self.add_item(
                InputText(
                    label="Name",
                    placeholder="Displayed name of the link",
                )
            )

            self.add_item(
                InputText(
                    label="URL",
                    placeholder="URL for the link",
                )
            )
            self.add_item(
                InputText(
                    label="Description",
                    placeholder="Describe where this link goes",
                    style=InputTextStyle.long,
                )
            )
            self.add_item(
                InputText(
                    label="Thumbnail", placeholder="URL for a thumbnail", required=False
                )
            )

        async def callback(self, interaction: Interaction):
            try:
                Link.objects.create(
                    name=self.children[0].value,
                    url=self.children[1].value,
                    description=self.children[2].value,
                    thumbnail=self.children[3].value,
                )
                msg = f"{self.children[0].value} has been added to the list of links"

                await interaction.response.send_message(msg, ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(e, ephemeral=True)
            self.stop()

    class EditModal(Modal):
        def __init__(self, name):
            super().__init__(title=f"Edit {name}")

            self.link1 = Link.objects.get(name=name)
            self.add_item(
                InputText(
                    label="Name",
                    placeholder="Displayed name of the link",
                    value=self.link1.name,
                )
            )

            self.add_item(
                InputText(
                    label="URL", placeholder="URL for the link", value=self.link1.url
                )
            )
            self.add_item(
                InputText(
                    label="Description",
                    placeholder="Describe where this link goes",
                    style=InputTextStyle.long,
                    value=self.link1.description,
                )
            )
            self.add_item(
                InputText(
                    label="Thumbnail",
                    placeholder="URL for a thumbnail",
                    required=False,
                    value=self.link1.thumbnail,
                )
            )

        async def callback(self, interaction: Interaction):
            try:
                self.link1.name = self.children[0].value
                self.link1.url = self.children[1].value
                self.link1.description = self.children[2].value
                self.link1.thumbnail = self.children[3].value
                self.link1.save()
                msg = f"{self.children[0].value} has been edited succesfully!"

                await interaction.response.send_message(msg, ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(e, ephemeral=True)
            self.stop()

    class DeleteModal(Modal):
        def __init__(self, name):
            super().__init__(title=f"Are you sure you want to delete {name}?")

            self.link1 = Link.objects.get(name=name)
            self.add_item(
                InputText(
                    label="Type 'yes' to confirm delete",
                    required=True,
                    min_length=3,
                    max_length=3,
                    style=InputTextStyle.short,
                )
            )

        async def callback(self, interaction: Interaction):
            try:
                name = self.link1.name
                self.link1.delete()
                msg = f"{name} has been deleted succesfully!"

                await interaction.response.send_message(msg, ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(e, ephemeral=True)
            self.stop()

    @links_commands.command(name="list", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("asmek_authcogs.manage_links")
    async def list(self, ctx):
        """
        list all current links
        """
        embed = Embed()
        embed.title = "All the links!!"
        embed.description = "A list of all links currently stored by the auth bot!"
        await ctx.defer(ephemeral=False)
        links = Link.objects.all()
        if links.count() > 0:
            for i in links:
                embed.add_field(name=f"{i.name}", value=i.url, inline=False)
        else:
            embed.description = "No Links added!"

        await ctx.respond(embed=embed, ephemeral=False)

    # //=============================================================================
    # // Add, edit, delete commands
    # //=============================================================================

    @links_commands.command(name="add", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("asmek_authcogs.manage_links")
    async def add(self, ctx):
        """
        add new link
        """
        add_modal = Links.AddModal()
        await ctx.send_modal(add_modal)

    @links_commands.command(name="edit", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("asmek_authcogs.manage_links")
    @option("name", description="Search for a Link!", autocomplete=search_links)
    async def edit(self, ctx, name: str):
        """
        edit link
        """
        edit_modal = Links.EditModal(name)
        await ctx.send_modal(edit_modal)

    @links_commands.command(name="delete", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @sender_has_perm("asmek_authcogs.manage_links")
    @option("name", description="Search for a Link!", autocomplete=search_links)
    async def delete(self, ctx, name: str):
        """
        delete link
        """
        delete_modal = Links.DeleteModal(name)
        await ctx.send_modal(delete_modal)

    @commands.slash_command(
        pass_context=True,
        description="Display a link",
        guild_ids=[int(settings.DISCORD_GUILD_ID)],
    )
    @option("name", description="Search for a Link!", autocomplete=search_links)
    async def link(self, ctx, name: str):
        """
        Display a link
        """
        try:
            link1 = Link.objects.get(name=name)
            embed = Embed(title=link1.name)
            if link1.thumbnail:
                embed.set_thumbnail(url=link1.thumbnail)
            embed.colour = Color.blurple()

            embed.description = link1.description

            embed.url = link1.url

            return await ctx.respond(embed=embed)
        except Link.DoesNotExist:
            return await ctx.respond(
                f"Link **{name}** does not exist in our Auth system"
            )
        except ObjectDoesNotExist:
            return await ctx.respond(f"**{name}** is does not exist")


def setup(bot):
    bot.add_cog(Links(bot))
