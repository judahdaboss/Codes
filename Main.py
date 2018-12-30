import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix=("!p"))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

@bot.event
async def on_member_join(member):
    server = member.server
    embed = discord.Embed(title="👋 {} just joined {} server!".format(member.name, server.name), description="Welcome to {} {}! Enjoy your stay here!".format(server.name, member.name), color=0x00ff00)
    embed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(discord.utils.get(server.channels, name = "joins-and-leaves"), embed=embed)

@bot.event
async def on_member_remove(member):
    server = member.server
    embed = discord.Embed(title="👋 {} just left the server.".format(member.name), description="Goodbye! {} hope to see you again".format(member.name), color=0x00ff00)
    embed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(discord.utils.get(server.channels, name = "joins-and-leaves"), embed=embed)
        
bot.run(os.environ['BOT_TOKEN'])
