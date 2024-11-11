from discord import app_commands, Interaction
from discord.ext import commands

from disckit.utils.help_util import load_help_embeds


class HelpCog(commands.Cog):
    """Help cog for the disckit library."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # @app_commands.command(description="Shows this command.")
    # async def help(self, interaction: Interaction, cog: str):
    #    """A fun coin flip command!"""


#
#    await load_help_embeds()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HelpCog(bot))
