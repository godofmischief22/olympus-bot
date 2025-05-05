import discord
from discord.ext import commands
from discord import app_commands, Interaction
from difflib import get_close_matches
from contextlib import suppress
from core import Context
from core.Sentinenl import Sentinel
from core.Cog import Cog
from utils.Tools import getConfig
from itertools import chain
import json
from utils import help as vhelp
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
import asyncio
from utils.config import serverLink
from utils.Tools import *

color = 0x000000
client = Sentinel()

class HelpCommand(commands.HelpCommand):

    async def send_ignore_message(self, ctx, ignore_type: str):
        if ignore_type == "channel":
            await ctx.reply(f"This channel is ignored.", mention_author=False)
        elif ignore_type == "command":
            await ctx.reply(f"{ctx.author.mention} This Command, Channel, or You have been ignored here.", delete_after=6)
        elif ignore_type == "user":
            await ctx.reply(f"You are ignored.", mention_author=False)

    async def on_help_command_error(self, ctx, error):
        errors = [
            commands.CommandOnCooldown, commands.CommandNotFound,
            discord.HTTPException, commands.CommandInvokeError
        ]
        if not type(error) in errors:
            await self.context.reply(f"Unknown Error Occurred\n{error.original}",
                                      mention_author=False)
        else:
            if type(error) == commands.CommandOnCooldown:
                return
        return await super().on_help_command_error(ctx, error)

    async def command_not_found(self, string: str) -> None:
        ctx = self.context
        check_ignore = await ignore_check().predicate(ctx)
        check_blacklist = await blacklist_check().predicate(ctx)

        if not check_blacklist:
            return

        if not check_ignore:
            await self.send_ignore_message(ctx, "command")
            return

        cmds = (str(cmd) for cmd in self.context.bot.walk_commands())
        matches = get_close_matches(string, cmds)

        embed = discord.Embed(
            title="",
            description=f"Command not found with the name `{string}`.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1275364856631005256.png")
        embed.set_author(name="Command Not Found", icon_url=self.context.bot.user.avatar.url)
        embed.set_footer(text=f"Requested By {ctx.author}",
                         icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        if matches:
            match_list = "\n".join([f"{index}. `{match}`" for index, match in enumerate(matches, start=1)])
            embed.add_field(name="Did you mean:", value=match_list, inline=True)

        await ctx.reply(embed=embed)

    async def send_bot_help(self, mapping):
        ctx = self.context
        check_ignore = await ignore_check().predicate(ctx)
        check_blacklist = await blacklist_check().predicate(ctx)

        if not check_blacklist:
            return

        if not check_ignore:
            await self.send_ignore_message(ctx, "command")
            return

        embed = discord.Embed(description="<a:RedLoading:1368481002254499931> **Loading Help module...**", color=color)
        ok = await self.context.reply(embed=embed)            
        data = await getConfig(self.context.guild.id)
        prefix = data["prefix"]
        filtered = await self.filter_commands(self.context.bot.walk_commands(),
                                              sort=True)
        slash = len([
            cmd for cmd in self.context.bot.tree.get_commands()  
            if isinstance(cmd, app_commands.Command)
        ])

        embed = discord.Embed(
            title="", color=0x000000)

        embed.add_field(
            name="**Bot Overview:**",
            value=(
                "```ansi\n"
                "<:prefix:1368486105275564083> : Server Prefix: **{prefix}**\n"
                "<:Commands:1368486421446393896> : Total Commands: **{len(set(self.context.bot.walk_commands()))}** | Slash: **{slash}**\n"
                "<:links:1368487179541549137> : *[Get Sentinel](https://discord.com/oauth2/authorize?client_id=1368135556784980051&permissions=8&integration_type=0&scope=bot+applications.commands)** | **[Support](https://discord.gg/xXqPVtZV7h)**\n"
                "```"
            ),
            inline=False
        )

        embed.add_field(
            name="**How do you use me?**",
            value=(
                "```ansi\n"
                ".help <command/module> for more info regarding that command/module!\n"
                "Example: .help mute\n"
                "```"
            ),
            inline=False
        )

        embed.add_field(
            name="**Main Modules:**",
            value=(
                "```ansi\n"
                "<:olympus_mod:1368122008381948008> : Security\n"
                "<:olympus_automode:1368489521502486610> : Emergency\n"
                "<:olympus_staff:1368489097689042964> : Moderation\n"
                "<:
