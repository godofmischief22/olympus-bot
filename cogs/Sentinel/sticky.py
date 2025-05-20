import discord
from discord.ext import commands


class Sticky(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    """Sticky Message"""

    def help_custom(self):
              emoji = '<:olympus_settings:1368131873951318056>'
              label = "Sticky Message"
              description = ""
              return emoji, label, description

    @commands.group()
    async def __Ignore__(self, ctx: commands.Context):
        """`stickyadd` , `stickyremove` , `stickyedit`"""
