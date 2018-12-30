import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=("m."))

@bot.event
async def on_member_join(member):
    server = member.server
    embed = discord.Embed(title="👋 {} just joined {} server!".format(member.name, server.name), description="Welcome to {} {}! Enjoy your stay here!".format(server.name, member.name), color=0x00ff00)
    embed.set_thumbnail(url=member.avatar_url)
    try:
        await bot.send_message(discord.utils.get(server.channels, name = "join-leave"), embed=embed)
    except discord.errors.InvalidArgument:
        await bot.create_channel(server, "join-leave", type=discord.ChannelType.text)
        await bot.send_message(discord.utils.get(server.channels, name="join-leave"), embed=embed)

@bot.event
async def on_member_remove(member):
    server = member.server
    embed = discord.Embed(title="👋 {} just left the server.".format(member.name), description="Goodbye! {} hope to see you again 😢".format(member.name), color=0x00ff00)
    embed.set_thumbnail(url=member.avatar_url)
    try:
        await bot.send_message(discord.utils.get(server.channels, name = "join-leave"), embed=embed)
    except discord.errors.InvalidArgument:
        await bot.create_channel(server, "join-leave", type=discord.ChannelType.text)
        await bot.send_message(discord.utils.get(server.channels, name="join-leave"), embed=embed)
        
bot.run(os.environ['BOT_TOKEN'])
