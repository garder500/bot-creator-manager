import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext
import re
import os
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.model import SlashCommandPermissionType
import psycopg2
import dotenv
import datetime

dotenv.load_dotenv()

time_re = re.compile(r"\d+[smhd]")

def get_time(time:str, index:int) -> int:
    sec = 0
    mult = 1
    for i in range(index-1, -1, -1):
        if not time[i].isdigit():
            return sec
        sec += int(time[i])*mult
        mult *= 10
    return sec

def calcul(time:str):
    if not bool(time_re.match(time)):
        return -1
    sec = 0
    x = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    for i in range(len(time)):
        if time[i] in x:
            sec += get_time(time, i) * x[time[i]]
    return sec

def setup(bot):
    bot.add_cog(GiveAway(bot))

class GiveAway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name = "test", guild_ids=[int(os.getenv("server_id"))], options=[
        create_option(
            name = "price",
            description="Which price",
            option_type=3,
            required=True
        ),
        create_option(
            name = "winners",
            description="How many winners ?",
            option_type=4,
            required=True
        ),
        create_option(
            name = "duration",
            description="Which duration (1d2h3m4s)",
            option_type=3,
            required=True
        )
    ])
    async def _test(self, ctx, price, winners, duration):
        msg = await ctx.send("message test")
        with psycopg2.connect(user="botmanager", password="pdjczAZ3Dw3H", host="149.91.80.94", port="5432", database="botmanager") as con:
            cursor = con.cursor()
            try:
                query = "SELECT * FROM giveaway"
                cursor.execute(query)
                result = cursor.fetchone()
                for item in result:
                    print(item)            
            except Exception as e:
                return print(e)
            await ctx.send("Requête sql effectué")


    @cog_ext.cog_slash(name = "giveaway", description="make a giveaway", guild_ids=[int(os.getenv("server_id"))], options=[
        create_option(
            name = "price",
            description="Which price",
            option_type=3,
            required=True
        ),
        create_option(
            name = "winners",
            description="How many winners ?",
            option_type=4,
            required=True
        ),
        create_option(
            name = "duration",
            description="Which duration (1d2h3m4s)",
            option_type=3,
            required=True
        )
    ])
    @cog_ext.permission(
    guild_id=int(os.getenv("server_id")),
    permissions=[
        create_permission(919356120466857984, SlashCommandPermissionType.ROLE, False),
        create_permission(528941015256530959, SlashCommandPermissionType.USER, True),
        create_permission(243117191774470146, SlashCommandPermissionType.USER, True),
        create_permission(405049567059640321, SlashCommandPermissionType.USER, True),
    ])
    async def _giveaway(self, ctx, price, winners, duration):
        embed = discord.Embed(title = f"{price}", description = f'{winners} winners', color = 0x0F056B)
        endtime = datetime.datetime.now() + datetime.timedelta(seconds = calcul(duration))
        await ctx.send(str(endtime))
        embed.add_field(name = f"Hosted by {ctx.author.name}#{ctx.author.discriminator}", value = f"End: <t:{round(datetime.datetime.timestamp(endtime))}:R>")
        message = await ctx.send(embed = embed)
        message.add_reaction("🎉")