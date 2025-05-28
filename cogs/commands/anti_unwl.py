import discord
from discord.ext import commands
import aiosqlite
from utils.Tools import *


class Unwhitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.initialize_db())

    #@commands.Cog.listener()
    async def initialize_db(self):
        self.db = await aiosqlite.connect('db/anti.db')

    @commands.hybrid_command(name='unwhitelist', aliases=['unwl'], help="Unwhitelist a user from antinuke")
    @commands.has_permissions(administrator=True)
    @blacklist_check()
    @ignore_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def unwhitelist(self, ctx, member: discord.Member = None):
        if ctx.guild.member_count < 2:
            embed = discord.Embed(
                color=0x000000,
                description="<:olympus_cross:1368120655643414548>| Your Server Doesn't Meet My 30 Member Criteria"
            )
            return await ctx.send(embed=embed)

        async with self.db.execute(
            "SELECT owner_id FROM extraowners WHERE guild_id = ? AND owner_id = ?",
            (ctx.guild.id, ctx.author.id)
        ) as cursor:
            check = await cursor.fetchone()

        async with self.db.execute(
            "SELECT status FROM antinuke WHERE guild_id = ?",
            (ctx.guild.id,)
        ) as cursor:
            antinuke = await cursor.fetchone()

        is_owner = ctx.author.id == ctx.guild.owner_id
        if not is_owner and not check:
            embed = discord.Embed(title="<:olympus_cross:1368120655643414548> Access Denied",
                color=0x000000,
                description="Only Server Owner or Extra Owner can Run this Command!"
            )
            return await ctx.send(embed=embed)

        if not antinuke or not antinuke[0]:
            embed = discord.Embed(
                color=0x000000,
                description=(
                    f"**{ctx.guild.name} Security Settings <:olympus_mod:1368122008381948008>\n"
                    "Ohh NO! looks like your server doesn't enabled security\n\n"
                    "Current Status : <:disabled:1368122132420362280>\n\n"
                    "To enable use `antinuke enable` **"
                )
            )
            return await ctx.send(embed=embed)

        if not member:
            embed = discord.Embed(
                color=0x000000,
                title="__**Unwhitelist Commands**__",
                description="**Removes user from whitelisted users which means that the antinuke module will now take actions on them if they trigger it.**"
            )
            embed.add_field(name="__**Usage**__", value="<:red_dot:1368122296451072072> `unwhitelist @user/id`\n<:red_dot:1368122296451072072> `unwl @user`")
            return await ctx.send(embed=embed)

        async with self.db.execute(
            "SELECT * FROM whitelisted_users WHERE guild_id = ? AND user_id = ?",
            (ctx.guild.id, member.id)
        ) as cursor:
            data = await cursor.fetchone()

        if not data:
            embed = discord.Embed(title="<:olympus_cross:1368120655643414548> Error",
                color=0x000000,
                description=f"<@{member.id}> is not a whitelisted member."
            )
            return await ctx.send(embed=embed)

        await self.db.execute(
            "DELETE FROM whitelisted_users WHERE guild_id = ? AND user_id = ?",
            (ctx.guild.id, member.id)
        )
        await self.db.commit()

        embed = discord.Embed(title="<:olympus_tick:1368119361440845824> Success",
            color=0x000000,
            description=f"User <@!{member.id}> has been removed from the whitelist."
        )
        await ctx.send(embed=embed)


"""
@Author: aadarshhhhh
    + Discord: aadarshhhhh
    + Community: https://discord.gg/6ffb6TpMH3 (Bitzxier Reborn)
    + for any queries reach out Community or DM me.
"""