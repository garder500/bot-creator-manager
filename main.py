import discord
from discord.ext import tasks, commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
import os
import dotenv
import datetime

dotenv.load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = "?!?!", intents = intents)
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands = True, sync_on_cog_reload = True)

@slash.slash(name = "reload", guild_ids=[int(os.getenv("server_id"))], description="Bot-Creator owner's commands", options=[
    create_option(
        name = "name",
        description="Name of the extension",
        option_type=3,
        required=True
    )
])
@slash.permission(
guild_id=int(os.getenv("server_id")),
permissions=[
    create_permission(919356120466857984, SlashCommandPermissionType.ROLE, False),
    create_permission(528941015256530959, SlashCommandPermissionType.USER, True),
    create_permission(243117191774470146, SlashCommandPermissionType.USER, True),
    create_permission(405049567059640321, SlashCommandPermissionType.USER, True),
])
async def _reload(ctx, name=None):
    if name == "main":
        return await ctx.send("You can't reload this extension", hidden=True)
    try:
        try:
            bot.unload_extension(f"cogs.{name}")
        except:
            pass
        bot.load_extension(f"cogs.{name}")
        await ctx.send(f"The extension **{name}.py** has beed reloaded by {ctx.author.mention}.", hidden=True)
    except:
        await ctx.send("This extension doesn't exist", hidden=True)

#on ready
@bot.event
async def on_ready():
    bot.load_extension("cogs.stats")
    print("prêt")
    await bot.change_presence(status=discord.Status.idle, activity = discord.Game(name="Welcome in Bot-Creator"))

lst = ["stats.py"]
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename not in lst:
        try:
            bot.load_extension(f"cogs.{filename[:len(filename)-3]}")
        except Exception as e:
            print(f"Impossible de changer {filename}: {e}")
bot.run(os.getenv("token"))