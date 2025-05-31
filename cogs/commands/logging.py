import discord
from discord.ext import commands
import sqlite3

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, guild):
        return discord.utils.get(guild.text_channels, name="veldrith-logs")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        log_channel = await self.get_log_channel(message.guild)
        if log_channel:
            embed = discord.Embed(
                title="馃棏锔� Message Deleted",
                description=f"**Author:** {message.author.mention}\n**Channel:** {message.channel.mention}\n**Content:** {message.content}",
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        log_channel = await self.get_log_channel(before.guild)
        if log_channel:
            embed = discord.Embed(
                title="鉁忥笍 Message Edited",
                description=f"**Author:** {before.author.mention}\n**Channel:** {before.channel.mention}",
                color=discord.Color.orange()
            )
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = await self.get_log_channel(member.guild)
        if log_channel:
            embed = discord.Embed(
                title="馃摜 Member Joined",
                description=f"{member.mention} joined the server.",
                color=discord.Color.green()
            )
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = await self.get_log_channel(member.guild)
        if log_channel:
            embed = discord.Embed(
                title="馃摛 Member Left",
                description=f"{member.mention} left or was kicked.",
                color=discord.Color.dark_red()
            )
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        log_channel = await self.get_log_channel(member.guild)
        if not log_channel:
            return

        if not before.channel and after.channel:
            action = f"馃帳 {member.mention} **joined** voice channel {after.channel.mention}"
        elif before.channel and not after.channel:
            action = f"馃攪 {member.mention} **left** voice channel {before.channel.mention}"
        elif before.channel != after.channel:
            action = f"馃攢 {member.mention} **moved** from {before.channel.mention} to {after.channel.mention}"
        else:
            return

        await log_channel.send(embed=discord.Embed(description=action, color=discord.Color.blue()))

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = await self.get_log_channel(channel.guild)
        if log_channel:
            await log_channel.send(embed=discord.Embed(
                title="馃摜 Channel Created",
                description=f"**Name:** {channel.name} ({channel.mention})",
                color=discord.Color.green()
            ))

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = await self.get_log_channel(channel.guild)
        if log_channel:
            await log_channel.send(embed=discord.Embed(
                title="馃棏锔� Channel Deleted",
                description=f"**Name:** {channel.name}",
                color=discord.Color.red()
            ))

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log_channel = await self.get_log_channel(guild)
        if log_channel:
            await log_channel.send(embed=discord.Embed(
                title="馃毃 Member Banned",
                description=f"{user.mention} was banned from the server.",
                color=discord.Color.dark_red()
            ))

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        log_channel = await self.get_log_channel(role.guild)
        if log_channel:
            await log_channel.send(embed=discord.Embed(
                title="鈿狅笍 Role Deleted",
                description=f"Role `{role.name}` was deleted.",
                color=discord.Color.orange()
            ))

async def setup(bot):
    await bot.add_cog(Logging(bot))
  
