import discord
from discord.ext import commands, tasks
import asyncio
from discord.utils import get
from discord_slash import cog_ext
import os
import dotenv

dotenv.load_dotenv()

def setup(bot):
    bot.add_cog(BeBetaTester(bot))

class BeBetaTester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name = "bebetatester", guild_ids=[int(os.getenv("server_id"))])
    async def _bebetatester(self, ctx):
        betarole = discord.utils.get(ctx.guild.roles, name='Beta tester')
        for role in ctx.author.roles:
            if role.name == "Beta tester":
                await ctx.author.remove_roles(betarole)
                return await ctx.send("You are no longer a beta tester !", hidden=True)
        else:
            await ctx.author.add_roles(betarole)
            return await ctx.send("You're now a beta tester !", hidden=True)