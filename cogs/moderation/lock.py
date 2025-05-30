import discord
from discord.ext import commands
from discord import ui

class LockUnlockView(ui.View):
    def __init__(self, channel, author, ctx):
        super().__init__(timeout=120)
        self.channel = channel
        self.author = author
        self.ctx = ctx  
        self.message = None  

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("You are not allowed to interact with this!", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        for item in self.children:
            if item.label != "Delete":
                item.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception:
                pass

    @ui.button(label="Unlock", style=discord.ButtonStyle.success)
    async def unlock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.response.send_message(f"{self.channel.mention} has been unlocked.", ephemeral=True)

        embed = discord.Embed(
            description=f"<:olympusChannel:1368556454633803787> **Channel**: {self.channel.mention}\n<:olympusReason:1368554945649053737> **Status**: Unlocked\n<:olympusArrow:1368445572251516961> **Reason:** Unlock request by {self.author}",
            color=0x000000
        )
        embed.add_field(name="<:olympus_staff:1368489097689042964> **Moderator:**", value=self.ctx.author.mention, inline=False)
        embed.set_author(name=f"Successfully Unlocked {self.channel.name}", icon_url="https://cdn.discordapp.com/emojis/1222750301233090600.png")
        await self.message.edit(embed=embed, view=self)

        for item in self.children:
            if item.label != "Delete":
                item.disabled = True
        await self.message.edit(view=self)

    @ui.button(style=discord.ButtonStyle.gray, emoji="<:olympus_bin:1368497055194021918>")
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()


class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.from_rgb(0, 0, 0)

    @commands.hybrid_command(
        name="lock",
        help="Locks a channel to prevent sending messages.",
        usage="lock <channel>",
        aliases=["lockchannel"])
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def lock_command(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel 
        if channel.permissions_for(ctx.guild.default_role).send_messages is False:
            embed = discord.Embed(
                description=f"**<:olympusChannel:1368556454633803787> Channel**: {channel.mention}\n<:olympusReason:1368554945649053737> **Status**: Already Locked",
                color=self.color
            )
            embed.set_author(name=f"{channel.name} is Already Locked", icon_url="https://cdn.discordapp.com/emojis/1294218790082711553.png")
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            view = LockUnlockView(channel=channel, author=ctx.author, ctx=ctx)  
            message = await ctx.send(embed=embed, view=view)
            view.message = message
            return

        await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        embed = discord.Embed(
            description=f"<:olympusChannel:1368556454633803787> **Channel**: {channel.mention}\n<:olympusReason:1368554945649053737> **Status**: Locked\n<:olympusArrow:1368445572251516961> **Reason:** Lock request by {ctx.author}",
            color=self.color
        )
        embed.add_field(name="<:olympus_staff:1368489097689042964> **Moderator:**", value=ctx.author.mention, inline=False)
        embed.set_author(name=f"Successfully Locked {channel.name}", icon_url="https://cdn.discordapp.com/emojis/1222750301233090600.png")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        view = LockUnlockView(channel=channel, author=ctx.author, ctx=ctx)  
        message = await ctx.send(embed=embed, view=view)
        view.message = message


"""
@Author: aadarshhhhh 
    + Discord: aadarshhhhh 
    + Community: https://discord.gg/6ffb6TpMH3 (Bitzxier Reborn)
    + for any queries reach out Community or DM me.
"""