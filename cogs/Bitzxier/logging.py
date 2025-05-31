import discord
from discord.ext import commands


class _logging(commands.Cog):  # ✅ Renamed from _voice to _logging
    def __init__(self, bot):
        self.bot = bot

    """Logging commands"""

    def help_custom(self):
        emoji = '<:olympus_mic:1368448688346759249>'
        label = "Logging Commands"
        description = ""
        return emoji, label, description

    @commands.group()
    async def __loggging__(self, ctx: commands.Context):
        """
        `setuplogs`
        """
        pass  # ← Add your subcommands under this
