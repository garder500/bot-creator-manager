import discord
from discord.ext import commands, tasks
import asyncio
from discord.utils import get

def setup(bot):
    bot.add_cog(Bienvenue(bot))

class Bienvenue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name='Member')
        await member.add_roles(role)
        await member.guild.get_channel(926786915032772629).send(f"Welcome {member.mention} ! We're now {member.guild.member_count} members !")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await member.guild.get_channel(926786979671191602).send(f"Goodbye {member.mention} ! We're now {member.guild.member_count} members !")