from __future__ import annotations
from discord.ext import commands, tasks
import discord
import aiohttp
import json
import jishaku
import asyncio
import typing
from typing import List
import aiosqlite
from utils.config import OWNER_IDS
from utils import getConfig, updateConfig
from .Context import Context
from colorama import Fore, Style, init
import importlib
import inspect

init(autoreset=True)

extensions: List[str] = [
    "cogs"
]

class Bitzxier(commands.AutoShardedBot):

    def __init__(self, *arg, **kwargs):
        intents = discord.Intents.all()
        intents.presences = True
        intents.members = True
        super().__init__(command_prefix=self.get_prefix,
                         case_insensitive=True,
                         intents=intents,
                         status=discord.Status.do_not_disturb,
                         strip_after_prefix=True,
                         owner_ids=OWNER_IDS,
                         allowed_mentions=discord.AllowedMentions(
                             everyone=False, replied_user=False, roles=False),
                         sync_commands_debug=True,
                         sync_commands=True,
                         shard_count=2)

        # Rotating presence setup
        self.presences = [
            discord.Activity(type=discord.ActivityType.watching, name="Bitzxier Dominance"),
            discord.Game(name="Protecting Servers"),
            discord.Activity(type=discord.ActivityType.listening, name="Commands"),
            discord.Streaming(name="Fear The Watcher. Trust The Shield 🛡️", url="https://m.twitch.tv/discord/home")
        ]
        self.presence_index = 0

    async def setup_hook(self):
        await self.load_extensions()
        self.rotate_presence.start()  #Start loop task here

    async def load_extensions(self):
        for extension in extensions:
            try:
                await self.load_extension(extension)
                print(Fore.GREEN + Style.BRIGHT + f"Loaded extension: {extension}")
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT}Failed to load extension {extension}. {e}")
        print(Fore.GREEN + Style.BRIGHT + "*" * 20)

    @tasks.loop(seconds=10)
    async def rotate_presence(self):
        activity = self.presences[self.presence_index]
        await self.change_presence(status=discord.Status.online, activity=activity)
        self.presence_index = (self.presence_index + 1) % len(self.presences)

    async def send_raw(self, channel_id: int, content: str, **kwargs) -> typing.Optional[discord.Message]:
        await self.http.send_message(channel_id, content, **kwargs)

    async def invoke_help_command(self, ctx: Context) -> None:
        return await ctx.send_help(ctx.command)

    async def fetch_message_by_channel(self, channel: discord.TextChannel, messageID: int) -> typing.Optional[discord.Message]:
        async for msg in channel.history(
                limit=1,
                before=discord.Object(messageID + 1),
                after=discord.Object(messageID - 1),
        ):
            return msg

    async def get_prefix(self, message: discord.Message):
        if message.guild:
            guild_id = message.guild.id
            async with aiosqlite.connect('db/np.db') as db:
                async with db.execute("SELECT id FROM np WHERE id = ?", (message.author.id,)) as cursor:
                    row = await cursor.fetchone()
                    data = await getConfig(guild_id)
                    prefix = data["prefix"]
                    if row:
                        return commands.when_mentioned_or(prefix, '')(self, message)
                    else:
                        return commands.when_mentioned_or(prefix)(self, message)
        else:
            async with aiosqlite.connect('db/np.db') as db:
                async with db.execute("SELECT id FROM np WHERE id = ?", (message.author.id,)) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return commands.when_mentioned_or('$', '')(self, message)
                    else:
                        return commands.when_mentioned_or('')(self, message)

    async def on_message_edit(self, before, after):
        ctx: Context = await self.get_context(after, cls=Context)
        if before.content != after.content:
            if after.guild is None or after.author.bot:
                return
            if ctx.command is None:
                return
            if type(ctx.channel) == "public_thread":
                return
            await self.invoke(ctx)

def setup_bot():
    intents = discord.Intents.all()
    bot = Bitzxier(intents=intents)
    return bot
    
