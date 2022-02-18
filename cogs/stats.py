import os

import discord
import dotenv
from discord.ext import commands, tasks
from discord_slash import SlashCommand, cog_ext
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import (create_choice, create_option,
                                                 create_permission)

dotenv.load_dotenv()

def setup(bot):
    bot.add_cog(Stats(bot))

class Stats(commands.Cog):
    def __init__(self, bot):
        self.statscheck.start()
        self.bot = bot
    
    @cog_ext.cog_slash(name = "dz", description="dza", guild_ids=[919356120466857984])
    async def _dz(self, ctx):
        return await ctx.send("ok", hidden=True)

    @tasks.loop(seconds=600)
    async def statscheck(self):
        guild = self.bot.get_guild(int(os.getenv("server_id")))
        await self.bot.get_channel(926629007015944282).edit(name = f"{guild.member_count} members") #nb membres
        await self.bot.get_channel(926629025093406791).edit(name = f"{len(list(filter(lambda m: str(m.status) == 'idle', guild.members))) + len(list(filter(lambda m: str(m.status) == 'dnd', guild.members))) + len(list(filter(lambda m: str(m.status) == 'online', guild.members)))} members online") #nb membres en ligne
        await self.bot.get_channel(926629063777456209).edit(name = f"{guild.premium_subscription_count} boost(s)") #nb membres
