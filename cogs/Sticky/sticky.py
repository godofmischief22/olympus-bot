import discord
from discord.ext import commands
from contextlib import suppress

class Sticky(commands.Cog):
    __slots__ = ('bot', 'messages')

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.messages: dict[int, tuple[int, str]] = {}  # {channel_id: (message_id, content)}

    async def _send_or_replace(self, channel: discord.TextChannel, content: str):
        """Delete old sticky if present, then send a new one."""
        old = self.messages.get(channel.id)
        if old:
            with suppress(discord.HTTPException):
                msg = await channel.fetch_message(old[0])
                await msg.delete()
        msg = await channel.send(content)
        self.messages[channel.id] = (msg.id, content)

    @commands.command(name="sticky", help="Set or replace a sticky message in this channel.")
    @commands.has_permissions(manage_messages=True)
    async def sticky(self, ctx: commands.Context, *, content: str):
        await self._send_or_replace(ctx.channel, content)
        with suppress(discord.Forbidden):
            await ctx.message.delete()

    @commands.command(name="editsticky", help="Edit the current sticky message.")
    @commands.has_permissions(manage_messages=True)
    async def edit_sticky(self, ctx: commands.Context, *, content: str):
        entry = self.messages.get(ctx.channel.id)
        if not entry:
            await ctx.send("No sticky message is set in this channel.", delete_after=5)
            return
        with suppress(discord.HTTPException):
            msg = await ctx.channel.fetch_message(entry[0])
            await msg.edit(content=content)
        self.messages[ctx.channel.id] = (entry[0], content)
        with suppress(discord.Forbidden):
            await ctx.message.delete()

    @commands.command(name="removesticky", help="Remove the sticky message from this channel.")
    @commands.has_permissions(manage_messages=True)
    async def remove_sticky(self, ctx: commands.Context):
        entry = self.messages.pop(ctx.channel.id, None)
        if not entry:
            await ctx.send("No sticky message to remove.", delete_after=5)
            return
        with suppress(discord.HTTPException):
            msg = await ctx.channel.fetch_message(entry[0])
            await msg.delete()
        with suppress(discord.Forbidden):
            await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        entry = self.messages.get(message.channel.id)
        if not entry:
            return
        await self._send_or_replace(message.channel, entry[1])

# Modern async setup for discord.py 2.x+
async def setup(bot: commands.Bot):
    await bot.add_cog(Sticky(bot))
