import discord
from discord.ext import commands
from discord import app_commands, Interaction
from difflib import get_close_matches
from contextlib import suppress
from core import Context
from core.Bitzxier import Bitzxier
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
client = Bitzxier()

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

    embed.add_field(name="**__Bot Overview:__**",value= f"<:prefix:1368486105275564083> Server Prefix:  **{prefix}** \n<:Commands:1368486421446393896> Total Commands: **{len(set(self.context.bot.walk_commands()))}** | Slash : **{slash}**\n<:links:1368487179541549137> **[Get Bitzxier](https://discord.com/oauth2/authorize?client_id=1375072186351485029&permissions=2113268958&scope=bot)** | **[Support](https://discord.gg/6ffb6TpMH3)**\n<a:quest_fa:1374020077057347656>__**How do you use me?**__\n```{prefix}help <command/module> to get more info regarding that command/module\nFor example: {prefix}help antinuke```\n")

    embed.add_field(
    name="**__Main Modules:__**",
    value=f">>> <:olympus_mod:1368122008381948008> : Security\n<:olympus_automode:1368489521502486610> : Emergency\n<:olympus_staff:1368489097689042964> : Moderation\n<:olympus_utility:1368489251439902801> : Utility\n<:olympus_raidmode:1368489502787502161> : Automod\n<:olympus_welcome:1368489606479220849> : Welcoming\n<:olympus_autorespond:1368489881981948024> : Customroles\n<:olympus_music:1368489805968838688> : Music\n<:olympus_giveaways:1368490008339681280> : Giveaway\n<:olympus_verification:1368490595525464135> : Auto Roles\n<:olympus_fun:1368490615712776233> : Fun\n<:olympus_mic:1368448688346759249> : Voice\n<:olympus_settings:1368131873951318056> : Ignore Commands")

    embed.add_field(name="**Bitzxier**",value="**Fear The Watcher. Trust The Shield!!**")
    embed.set_footer(
      text=f"Requested By {self.context.author}",
      icon_url=self.context.author.avatar.url if self.context.author.avatar else self.context.author.default_avatar.url
    )
    embed.set_author(name=self.context.author, icon_url=self.context.author.avatar.url if self.context.author.avatar else self.context.author.default_avatar.url)

    #embed.timestamp = discord.utils.utcnow()
    view = vhelp.View(mapping=mapping,
                          ctx=self.context,
                          homeembed=embed,
                          ui=2)
    await asyncio.sleep(0.5)
    await ok.edit(embed=embed,view=view)



  
  async def send_command_help(self, command):
    ctx = self.context
    check_ignore = await ignore_check().predicate(ctx)
    check_blacklist = await blacklist_check().predicate(ctx)

    if not check_blacklist:
      return

    if not check_ignore:
      await self.send_ignore_message(ctx, "command")
      return
    
    sonu = f">>> {command.help}" if command.help else '>>> No Help Provided...'
    embed = discord.Embed(
        description=
        f"""```xml
<[] = optional | () = required\nDon't type these while using Commands>```\n{sonu}""",
        color=color)
    alias = ' | '.join(command.aliases)

    embed.add_field(name="**Aliases**",
                      value=f"{alias}" if command.aliases else "No Aliases",
                      inline=False)
    embed.add_field(name="**Usage**",
                      value=f"`{self.context.prefix}{command.signature}`\n")
    embed.set_author(name=f"{command.qualified_name.title()} Command",
                       icon_url=self.context.bot.user.display_avatar.url)
    await self.context.reply(embed=embed, mention_author=False)

  def get_command_signature(self, command: commands.Command) -> str:
    parent = command.full_parent_name
    if len(command.aliases) > 0:
      aliases = ' | '.join(command.aliases)
      fmt = f'[{command.name} | {aliases}]'
      if parent:
        fmt = f'{parent}'
      alias = f'[{command.name} | {aliases}]'
    else:
      alias = command.name if not parent else f'{parent} {command.name}'
    return f'{alias} {command.signature}'

  def common_command_formatting(self, embed_like, command):
    embed_like.title = self.get_command_signature(command)
    if command.description:
      embed_like.description = f'{command.description}\n\n{command.help}'
    else:
      embed_like.description = command.help or 'No help found...'

  async def send_group_help(self, group):
    ctx = self.context
    check_ignore = await ignore_check().predicate(ctx)
    check_blacklist = await blacklist_check().predicate(ctx)

    if not check_blacklist:
        return

    if not check_ignore:
        await self.send_ignore_message(ctx, "command")
        return

    entries = [
        (
            f"➜ `{self.context.prefix}{cmd.qualified_name}`\n",
            f"{cmd.short_doc if cmd.short_doc else ''}\n\u200b"
        )
        for cmd in group.commands
    ]

    count = len(group.commands)

    embeds = FieldPagePaginator(
        entries=entries,
        title=f"{group.qualified_name.title()} [{count}]",
        description="< > Duty | [ ] Optional\n",
        per_page=4
    ).get_pages()

    paginator = Paginator(ctx, embeds)
    await paginator.paginate()
    
  async def send_cog_help(self, cog):
    ctx = self.context
    check_ignore = await ignore_check().predicate(ctx)
    check_blacklist = await blacklist_check().predicate(ctx)

    if not check_blacklist:
      return

    if not check_ignore:
      await self.send_ignore_message(ctx, "command")
      return


    entries = [(
      f"➜ `{self.context.prefix}{cmd.qualified_name}`",
      f"{cmd.short_doc if cmd.short_doc else ''}"
      f"\n\u200b",
    ) for cmd in cog.get_commands()]
    embeds = FieldPagePaginator(
      entries=entries,
      title=f"{cog.qualified_name.title()} ({len(cog.get_commands())})",
      description="< > Duty | [ ] Optional\n\n",
      color=color,
      per_page=4).get_pages()
    paginator = Paginator(ctx, embeds)
    await paginator.paginate()


class Help(Cog, name="help"):

  def __init__(self, client: Bitzxier):
    self._original_help_command = client.help_command
    attributes = {
      'name':
      "help",
      'aliases': ['h'],
      'cooldown':
      commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user),
      'help':
      'Shows help about bot, a command or a category'
    }
    client.help_command = HelpCommand(command_attrs=attributes)
    client.help_command.cog = self

  async def cog_unload(self):
    self.help_command = self._original_help_command
    
