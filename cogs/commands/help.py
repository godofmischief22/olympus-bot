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

  async def send\_ignore\_message(self, ctx, ignore\_type: str):

    if ignore\_type == "channel":
      await ctx.reply(f"This channel is ignored.", mention\_author=False)
    elif ignore\_type == "command":
      await ctx.reply(f"{ctx.author.mention} This Command, Channel, or You have been ignored here.", delete\_after=6)
    elif ignore\_type == "user":
      await ctx.reply(f"You are ignored.", mention\_author=False)

  async def on\_help\_command\_error(self, ctx, error):
    errors = \[
      commands.CommandOnCooldown, commands.CommandNotFound,
      discord.HTTPException, commands.CommandInvokeError
    ]
    if not type(error) in errors:
      await self.context.reply(f"Unknown Error Occurred\n{error.original}",
                               mention\_author=False)
    else:
      if type(error) == commands.CommandOnCooldown:
        return

    return await super().on\_help\_command\_error(ctx, error)

  
  async def command\_not\_found(self, string: str) -> None:
    ctx = self.context
    check\_ignore = await ignore\_check().predicate(ctx)
    check\_blacklist = await blacklist\_check().predicate(ctx)

    if not check\_blacklist:
        return

    if not check\_ignore:
        await self.send\_ignore\_message(ctx, "command")
        return

    cmds = (str(cmd) for cmd in self.context.bot.walk\_commands())
    matches = get\_close\_matches(string, cmds)

    embed = discord.Embed(
        title="",
        description=f"Command not found with the name `{string}`.",
        color=discord.Color.red()
    )
    embed.set\_thumbnail(url="[https://cdn.discordapp.com/emojis/1275364856631005256.png](https://cdn.discordapp.com/emojis/1275364856631005256.png)")
    embed.set\_author(name="Command Not Found", icon\_url=self.context.bot.user.avatar.url)
    embed.set\_footer(text=f"Requested By {ctx.author}",
                       icon\_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default\_avatar.url)
    if matches:
        match\_list = "\n".join(\[f"{index}. `{match}`" for index, match in enumerate(matches, start=1)])
        embed.add\_field(name="Did you mean:", value=match\_list, inline=True)

    await ctx.reply(embed=embed)

  
  async def send\_bot\_help(self, mapping):
    ctx = self.context
    check\_ignore = await ignore\_check().predicate(ctx)
    check\_blacklist = await blacklist\_check().predicate(ctx)

    if not check\_blacklist:
      return

    if not check\_ignore:
      await self.send\_ignore\_message(ctx, "command")
      return

    
    embed = discord.Embed(description="\<a\:RedLoading:1368481002254499931> **Loading Help module...**", color=color)
    ok = await self.context.reply(embed=embed)          
    data = await getConfig(self.context.guild.id)
    prefix = data\["prefix"]
    filtered = await self.filter\_commands(self.context.bot.walk\_commands(),
                                              sort=True)
    slash = len(\[
  cmd for cmd in self.context.bot.tree.get\_commands() 
  if isinstance(cmd, app\_commands.Command)
])
    
    embed = discord.Embed(
      title="", color=0x000000)

    embed.add\_field(
    name="**Bot Overview:**",
    value=(
        f"`ansi\n"
        f"<:prefix:1368486105275564083> : Server Prefix: **{prefix}**\n"
        f"<:Commands:1368486421446393896> : Total Commands: **{len(set(self.context.bot.walk_commands()))}** | Slash: **{slash}**\n"
        f"<:links:1368487179541549137> : *[Get Sentinel](https://discord.com/oauth2/authorize?client_id=1368135556784980051&permissions=8&integration_type=0&scope=bot+applications.commands)** | **[Support](https://discord.gg/xXqPVtZV7h)**\n"
        f"`"
    ),
    inline=False
)

embed.add\_field(
    name="**How do you use me?**",
    value=(
        "`ansi\n"
        ".help <command/module> for more info regarding that command/module!\n"
        "Example: .help mute\n"
        "`"
    ),
    inline=False
)

embed.add\_field(
    name="**Main Modules:**",
    value=(
        "`ansi\n"
        "<:olympus_mod:1368122008381948008> : Security\n"
        "<:olympus_automode:1368489521502486610> : Emergency\n"
        "<:olympus_staff:1368489097689042964> : Moderation\n"
        "<:olympus_utility:1368489251439902801> : Utility\n"
        "<:olympus_raidmode:1368489502787502161> : Automod\n"
        "<:olympus_welcome:1368489606479220849> : Welcoming\n"
        "<:olympus_autorespond:1368489881981948024> : Customroles\n"
        "<:olympus_music:1368489805968838688> : Music\n"
        "<:olympus_giveaways:1368490008339681280> : Giveaway\n"
        "<:Camera:1368490184970338385> : Camera Enforcement\n"
        "<:Star:1368492678270156911> : Boycott/VcBan\n"
        "<:olympus_verification:1368490595525464135> : Auto Roles\n"
        "<:olympus_fun:1368490615712776233> : Fun\n"
        "<:olympus_mic:1368448688346759249> : Voice\n"
        "<:olympus_settings:1368131873951318056> : Ignore Commands\n"
        "`"
    ),
    inline=False
)
embed.add\_field(
    name="Need Help?",
    value="**Use buttons to swap pages & menu to select help pages. Need help? [Contact Support.](https://discord.gg/xXqPVtZV7h)**",
    inline=False
)

embed.set\_footer(
    text=f"Requested By {self.context.author}",
    icon\_url=self.context.author.avatar.url if self.context.author.avatar else self.context.author.default\_avatar.url
)

embed.set\_author(
    name=str(self.context.author),
    icon\_url=self.context.author.avatar.url if self.context.author.avatar else self.context.author.default\_avatar.url
)

# Optional: Uncomment to add timestamp

# embed.timestamp = discord.utils.utcnow()

view = vhelp.View(
    mapping=mapping,
    ctx=self.context,
    homeembed=embed,
    ui=2
)

await asyncio.sleep(0.5)
await ok.edit(embed=embed, view=view)
  
  async def send\_command\_help(self, command):
    ctx = self.context
    check\_ignore = await ignore\_check().predicate(ctx)
    check\_blacklist = await blacklist\_check().predicate(ctx)

    if not check\_blacklist:
      return

    if not check\_ignore:
      await self.send\_ignore\_message(ctx, "command")
      return
    
    sonu = f">>> {command.help}" if command.help else '>>> No Help Provided...'
    embed = discord.Embed(
        description=
        f"""`xml
<[] = optional | 鈥光€� = required\nDon't type these while using Commands>`\n{sonu}""",
        color=color)
    alias = ' | '.join(command.aliases)

    embed.add\_field(name="**Aliases**",
                      value=f"{alias}" if command.aliases else "No Aliases",
                      inline=False)
    embed.add\_field(name="**Usage**",
                      value=f"`{self.context.prefix}{command.signature}`\n")
    embed.set\_author(name=f"{command.qualified\_name.title()} Command",
                       icon\_url=self.context.bot.user.display\_avatar.url)
    await self.context.reply(embed=embed, mention\_author=False)

  def get\_command\_signature(self, command: commands.Command) -> str:
    parent = command.full\_parent\_name
    if len(command.aliases) > 0:
      aliases = ' | '.join(command.aliases)
      fmt = f'\[{command.name} | {aliases}]'
      if parent:
        fmt = f'{parent}'
      alias = f'\[{command.name} | {aliases}]'
    else:
      alias = command.name if not parent else f'{parent} {command.name}'
    return f'{alias} {command.signature}'

  def common\_command\_formatting(self, embed\_like, command):
    embed\_like.title = self.get\_command\_signature(command)
    if command.description:
      embed\_like.description = f'{command.description}\n\n{command.help}'
    else:
      embed\_like.description = command.help or 'No help found...'

  async def send\_group\_help(self, group):
    ctx = self.context
    check\_ignore = await ignore\_check().predicate(ctx)
    check\_blacklist = await blacklist\_check().predicate(ctx)

    if not check\_blacklist:
        return

    if not check\_ignore:
        await self.send\_ignore\_message(ctx, "command")
        return

    entries = \[
        (
            f"鉃� `{self.context.prefix}{cmd.qualified_name}`\n",
            f"{cmd.short\_doc if cmd.short\_doc else ''}\n\u200b"
        )
        for cmd in group.commands
    ]

    count = len(group.commands)

    embeds = FieldPagePaginator(
        entries=entries,
        title=f"{group.qualified\_name.title()} \[{count}]",
        description="< > Duty | \[ ] Optional\n",
        per\_page=4
    ).get\_pages()

    paginator = Paginator(ctx, embeds)
    await paginator.paginate()
    
  async def send\_cog\_help(self, cog):
    ctx = self.context
    check\_ignore = await ignore\_check().predicate(ctx)
    check\_blacklist = await blacklist\_check().predicate(ctx)

    if not check\_blacklist:
      return

    if not check\_ignore:
      await self.send\_ignore\_message(ctx, "command")
      return

    entries = \[(
      f"鉃� `{self.context.prefix}{cmd.qualified_name}`",
      f"{cmd.short\_doc if cmd.short\_doc else ''}"
      f"\n\u200b",
    ) for cmd in cog.get\_commands()]
    embeds = FieldPagePaginator(
      entries=entries,
      title=f"{cog.qualified\_name.title()} ({len(cog.get\_commands())})",
      description="< > Duty | \[ ] Optional\n\n",
      color=color,
      per\_page=4).get\_pages()
    paginator = Paginator(ctx, embeds)
    await paginator.paginate()

class Help(Cog, name="help"):

  def **init**(self, client: Sentinel):
    self.\_original\_help\_command = client.help\_command
    attributes = {
      'name':
      "help",
      'aliases': \['h'],
      'cooldown':
      commands.CooldownMapping.from\_cooldown(1, 5, commands.BucketType.user),
      'help':
      'Shows help about bot, a command or a category'
    }
    client.help\_command = HelpCommand(command\_attrs=attributes)
    client.help\_command.cog = self

  async def cog\_unload(self):
    self.help\_command = self.\_original\_help\_command

Fix all issues and send don't change emojis and other

    
