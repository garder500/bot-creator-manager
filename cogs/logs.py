from discord.ext import commands, tasks
import os
import discord
import dotenv
import datetime

dotenv.load_dotenv()

def setup(bot):
    bot.add_cog(Logs(bot))

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        async for entry in message.guild.audit_logs(limit=1,action=discord.AuditLogAction.message_delete):
            print(entry.message)
            deleter = entry
        embed = discord.Embed(title = "Message deleted", color = 0xFF0000)
        embed.add_field(name = "Author", value = f"{message.author.mention} ({message.author.id})", inline=True)
        # embed.add_field(name = "Deleted by", value = f'{deleter.user.mention} ({deleter.user.id})') if deleter. else embed.add_field(name = "Deleted by", value = f'{message.author.mention} ({message.author.id})')
        embed.add_field(name = "Deleter is a staff ?", value = "Mod" if (deleter.user.guild_permissions.value & (1 << 3)) == 1 << 3 else "User")
        embed.add_field(name = "Channel", value = f"{message.channel.mention} ({message.channel.id})", inline=True)
        if len(message.attachments) > 0:
            for i in range(len(message.attachments)):
                embed.add_field(name = f"Image #{i+1}", value = message.attachments[i].url)
        if len(message.content) > 0:
            embed.add_field(name = "Value", value = message.content, inline=True)
        embed.add_field(name = "Time", value = f"<t:{str(int(datetime.datetime.timestamp(datetime.datetime.now())))}:R>", inline=True)
        channel = self.bot.get_channel(int(os.getenv("logs_channel")))
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        try:
            embed = discord.Embed(title = "Message edited", color = 0xFFA500)
            embed.add_field(name = "Author", value = f"{message_before.author.mention} ({message_before.author.id})", inline=True)
            embed.add_field(name = "Channel", value = f"{message_before.channel.mention} ({message_before.channel.id})", inline=True)
            embed.add_field(name = "Value", value = f'{message_before.content}\n=>\n{message_after.content}', inline=True)
            embed.add_field(name = "Time", value = f"<t:{str(int(datetime.datetime.timestamp(datetime.datetime.now())))}:R>", inline=True)
            channel = self.bot.get_channel(int(os.getenv("logs_channel")))
            await channel.send(embed = embed)
        except:
            pass