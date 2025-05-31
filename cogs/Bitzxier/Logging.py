import discord
from discord.ext import commands


class _voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Logging commands"""
  
    def help_custom(self):
		      emoji = '<:olympus_mic:1368448688346759249>'
		      label = "Logging Commands"
		      description = ""
		      return emoji, label, description

    @commands.group()
    async def __Loggging__(self, ctx: commands.Context):
        """
        `setuplogs`"""
