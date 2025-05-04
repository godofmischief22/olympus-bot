import discord
from discord.ext import commands
import asyncio

class React(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        for owner in self.bot.owner_ids:
            if f"<@{owner}>" in message.content:
                try:
                    if owner == 1131806691969728593:
                        
                        emojis = [
                            "<a:owner:1368576266260840488>",
                            "<:7club_ban:1368576416899137639>",
                            "<:land_yildiz:1368576543307333774>",
                            "<a:_rose:1368576634982240368>",
                            "<:land_yildiz:1368576543307333774>",
                            "<a:37496alert:1368576794776830023>",
                            "<:sq_HeadMod:1368576904663273488>",
                            "<:Dc_RedCrownEsports:1368576985072275557>",
                            "<a:GIFD:1368577097660108890>",
                            "<a:GIFN:1368577219210903583>",
                            "<a:max__A:1368578036395675769>",
                            "<:Heeriye:1368578228360319076>",
                            "<:heart_em:1368578372162027661>",
                            "a:star:1368577472727355543>",
                            "<a:king:1368578500901998642>",
                            "<:headmod:1368578621366603906>",
                            "<a:sg_rd:1368578700840538202>",
                            "<a:RedHeart:1368577595750481950>",
                            " <a:star:1368577472727355543>"
                        ]
                        for emoji in emojis:
                            await message.add_reaction(emoji)
                    else:
                        
                        await message.add_reaction("<a:owner:1368576266260840488>")
                except discord.errors.RateLimited as e:
                    await asyncio.sleep(e.retry_after)
                    await message.add_reaction("<a:owner:1368576266260840488>")
                except Exception as e:
                    print(f"An unexpected error occurred Auto react owner mention: {e}")
