import discord

from discord.ext import commands
from typing import Tuple, List, Dict

from disckit.errors import InvalidHelpCog
from disckit.config import UtilConfig

_help_embeds: Dict[str, discord.Embed] = {}
_app_commands: Dict[str, discord.app_commands.AppCommand] = {}


async def load_help_embeds(
    bot: commands.Bot, cog: str, cmds_per_embed: int = 7, update: bool = False
) -> List[discord.Embed]:
    """A function which returns a list of commands along with their descriptions
    from the requested command cog as a list of embeds.

    Parameters
    ----------
    bot : :class:`Bot`
        The :class:`commands.Bot` object used to walk thorugh the bot's commands.

    cog : :class:`str`
        The command cog you want.

    cmds_per_embed : :class:`int`
        Number of commands to be present in each embed.
    """
    #global _app_commands

    if cog not in bot.cogs:
        raise InvalidHelpCog(
            f"Failed loading cog: {cog} among the cogs: {bot.cogs}", cog=cog
        )

    # if _help_embeds[cog] is not None and not update:
    #    return _help_embeds[cog]

    for app_cmd in  await bot.tree.fetch_commands():
        _app_commands[app_cmd.name] = app_cmd

    embeds: List[discord.Embed] = []
    descriptions: List[str] = []
    counter = 1
    cog_name = cog.lower()

    print("\n\nBOT COMMANDS: ", _app_commands, "\n\n")

    # for cmd in bot_commands:
    for cmd in bot.get_cog(cog).walk_app_commands():
        # if cog_name in cmd.name:
        print("ADDING COMMAND: ", cmd, "\n\n")
        command_mention = _app_commands.get(cmd.name)
        if command_mention is None:
            command_mention = cmd.name
        else:
            command_mention = command_mention.mention

        descriptions.append(f"`{counter}.` {command_mention}" f"\n> {cmd.description}")
        counter += 1

        if counter % cmds_per_embed == 0:
            embed = discord.Embed(
                title=f"{cog} Commands",
                colour=UtilConfig.HELP_COLOR,
                description="\n\n".join(descriptions),
            )
            embeds.append(embed)
            descriptions.clear()

    if len(descriptions) > 0:
        embed = discord.Embed(
            title=f"{cog_name.title()} Commands",
            colour=UtilConfig.HELP_COLOR,
            description="\n\n".join(descriptions),
        )
        embeds.append(embed)

    _help_embeds[cog] = embeds
    return embeds
