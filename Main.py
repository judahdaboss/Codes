import discord
from discord.ext import commands
import inspect
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
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
    await bot.send_message(discord.utils.get(server.channels, name = "joins-and-leaves"), embed=embed)

@bot.event
async def on_member_remove(member):
    server = member.server
    embed = discord.Embed(title="👋 {} just left the server.".format(member.name), description="Goodbye! {} hope to see you again".format(member.name), color=0x00ff00)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
    await bot.send_message(discord.utils.get(server.channels, name = "joins-and-leaves"), embed=embed)
    
def user_is_me(ctx):
	return ctx.message.author.id == "277983178914922497"
    
@bot.command(name='eval', pass_context=True)
@commands.check(user_is_me)
async def _eval(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await bot.say(await res)
    else:
    	await bot.delete_message(ctx.message)
    	await bot.say(res)
        
bot.run(os.environ['BOT_TOKEN'])
