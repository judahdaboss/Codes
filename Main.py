import discord
from discord.ext import commands
import asyncio
import time
import random
import inspect
import json
import os

client = commands.Bot(command_prefix=("!p"))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_member_join(member):
    server = member.server
    embed = discord.Embed(title="👋 {} just joined {}".format(member.name, server.name), description="Welcome! to {} {}! Enjoy your stay here!".format(server.name, member.name), color=0x00ff00)
    embed.set_thumbnail(url=member.avatar_url)
    try:
        await client.send_message(discord.utils.get(server.channels, name = "joins-and-leaves"), embed=embed)
    except discord.errors.InvalidArgument:
        await client.create_channel(server, "joins-and-leaves", type=discord.ChannelType.text)
        await client.send_message(discord.utils.get(server.channels, name="joins-and-leaves"), embed=embed)

@client.event
async def on_member_remove(member):
    server = member.server
    embed = discord.Embed(title="👋 {} just left the server.".format(member.name), description="Goodbye! {} hope to see you again".format(member.name), color=0x00ff00)
    embed.set_thumbnail(url=member.avatar_url)
    try:
        await client.send_message(discord.utils.get(server.channels, name = "joins-and-leaves"), embed=embed)
    except discord.errors.InvalidArgument:
	await client.create_channel(server, "joins-and-leave", type=discord.ChannelType.text)
	await client.send_message(discord.utils.get(server.channels, name="joins-and-leaves"), embed=embed)
   
@client.event
async def on_message(message):
	if message.content.upper().startswith('!P8BALL'):
		ball8 = ([':8ball: It is certain',':8ball: As i see it, yes', ':8ball: Dont count on it', ':8ball: Without a doubt', ':8ball: Definitely', ':8ball: Very doubtful', ':8ball: Outlook not so good', ':8ball: My sources say no', ':8ball: My reply is no', ':8ball: Most likely', ':8ball: You may rely on it', ':8ball: Ask again later'])
		await client.send_message(message.channel,(random.choice(ball8)))
	await client.process_commands(message)
    
def user_is_me(ctx):
	return ctx.message.author.id == "277983178914922497"
    
@client.command(name='eval', pass_context=True)
@commands.check(user_is_me)
async def _eval(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await client.say(await res)
    else:
    	await client.delete_message(ctx.message)
    	await client.say(res)
        
client.run(os.environ['BOT_TOKEN'])
