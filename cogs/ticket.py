import discord
from discord.ext import commands
from discord_slash import cog_ext
import re
import os
from discord_slash.utils.manage_commands import create_option
import dotenv

dotenv.load_dotenv()

member_re = re.compile(r"[\D]")

def setup(bot):
    bot.add_cog(Ticket(bot))

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name = "ticket", description="Make a ticket for help", guild_ids=[int(os.getenv("server_id"))])
    async def _ticket(self, ctx):
        category = self.bot.get_channel(926637276463779881)
        for chan in category.text_channels:
            if chan.topic and str(ctx.author.id) in chan.topic:
                return await ctx.send("You already have an open channel", hidden=True)
        newchan = await ctx.guild.create_text_channel(category = category, name = f"{ctx.author.name}'s-ticket", topic = f"{ctx.author.mention}'s ticket")
        await newchan.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)

        for role in ctx.guild.roles:
            if role.name.lower() == "staff":
                await newchan.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                break
        
        await newchan.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        await ctx.send(f"Your channel has been created ! ({newchan.mention})", hidden=True)

        embed = discord.Embed(title = f"{ctx.author}'s Ticket")
        embed.add_field(name = "**__Get help quickly__**", value = "\u200b")
        embed.add_field(name = "For it", value = "Please explain the problem, and attach screens if possible", inline = False)
        embed.add_field(name = "The different commands", value = "> /close: close the ticket \n> /add (id / mention): add someone to the ticket \n> /remove (id / mention): remove someone from the ticket", inline = False)
        await newchan.send(embed = embed)


    @cog_ext.cog_slash(name = "close", description="Close a ticket", guild_ids=[int(os.getenv("server_id"))])
    async def _close(self, ctx):
        if ctx.channel.name.endswith("s-ticket"):
            for role in ctx.author.roles:
                if role.permission.administrator:
                    file = await self.getlogs(ctx)
                    embed = discord.Embed(title = "Tickets logs", color = 0xBB0B0B)
                    member = ctx.guild.get_member(int(member_re.sub("" ,ctx.channel.topic)))
                    embed.add_field(name = "User", value = f"{member.mention} ({member.id})", inline=True)
                    embed.add_field(name = "Moderator", value = f"{ctx.author.mention} ({ctx.author.id})", inline=True)
                    with open(file.name, "rb") as file:
                        await ctx.guild.get_channel(int(os.getenv("tickets_logs"))).send(embed = embed, file = discord.File(file))
                    await ctx.channel.delete(reason = "Closed by a staff") 
                    return os.remove(os.getcwd() + f'/{file.name}')
        
            if str(ctx.author.id) in ctx.channel.topic: 
                file = await self.getlogs(ctx)
                embed = discord.Embed(title = "Tickets logs", color = 0xBB0B0B)
                embed.add_field(name = "User", value = f"{ctx.author.mention} ({ctx.author.id})", inline=True)
                embed.add_field(name = "Moderator", value = f"{ctx.author.mention} ({ctx.author.id})", inline=True)
                with open(file.name, "rb") as file:
                    await ctx.guild.get_channel(int(os.getenv("tickets_logs"))).send(embed = embed, file = discord.File(file))
                await ctx.channel.delete(reason = "Closed by the user")
                return os.remove(os.getcwd() + f'/{file.name}')
            
            return await ctx.send("You don't have the permission to close this channel", hidden=True)
    

        else:
            return await ctx.send("You're not inside a ticket", hidden=True)

    
    async def getlogs(self, ctx):
        file = open(f"{ctx.channel.name[:-8]}.txt", "w+")
        msg = [message for message in await ctx.channel.history().flatten()]
        msg.reverse()
        for message in msg:
            if message.content:
                file.write(f'[{message.created_at.strftime("%d/%m/%Y %H:%M:%S")}] {message.author.name}#{message.author.discriminator} => {message.content}\n')
        return file

    

    @cog_ext.cog_slash(name = "add", description="Add someone inside your ticket", guild_ids=[int(os.getenv("server_id"))], options=[
        create_option(
            name = "member",
            description="Which member",
            option_type=6,
            required=True
        )
    ])
    async def _add(self, ctx, member):
        if not ctx.channel.name.endswith("s-ticket"):
            return await ctx.send("You must be in a ticket", hidden=True)
        if str(ctx.author.id) in ctx.channel.topic or ctx.author.guild_permissions.administrator:
            for targ in ctx.channel.members:
                if member == targ:
                    return await ctx.send(f"{member.mention} is already on this ticket", hidden=True)
            await ctx.channel.set_permissions(member, send_messages=True, read_messages=True)
            return await ctx.send(f"{member.mention} has been added to the ticket")

        else:
            return await ctx.send("You are not the owner of this channel and you're not an administrator")

    @cog_ext.cog_slash(name = "remove", description="Remove someone from your ticket", guild_ids=[int(os.getenv("server_id"))], options=[
        create_option(
            name = "member",
            description="Which member",
            option_type=6,
            required=True
        )
    ])    
    async def _remove(self, ctx, member = None):
        if not ctx.channel.name.endswith("s-ticket"):
            return await ctx.send("You must be in a ticket", hidden=True)
        if str(ctx.author.id) in ctx.channel.topic or ctx.author.guild_permissions.administrator:
            if member.id == ctx.author.id:
                return await ctx.send("You cannot kick yourself out of this ticket", hidden=True)
            if member.guild_permissions.administrator:
                return await ctx.send("You cannot remove that person from this channel", hidden=True)
            try:
                await ctx.channel.set_permissions(member, send_messages=False, read_messages=False)
                return await ctx.send(f"{member.mention} has been removed from the ticket")
            except:
                await ctx.send("This user is not on the ticket", hidden=True)

        else:
            return await ctx.send("You are not the owner of this channel", hidden=True)
