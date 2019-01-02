import discord
from discord.ext import commands
import inspect
import random
import os
import asyncio
import json
import os
import bs4, requests
from discord import opus
import youtube_dl

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
        await client.create_channel(server, "joins-and-leaves", type=discord.ChannelType.text)
        await client.send_message(discord.utils.get(server.channels, name="joins-and-leaves"), embed=embed)
	
@client.event
async def on_message(message):
  if message.content == 'm.skip':
      serverid = message.server.id
      players[serverid].stop()
  if message.content == 'm.pause':
      serverid = message.server.id
      players[serverid].pause()
      await client.send_message(message.channel, "Player paused")
  if message.content == 'm.resume':
      serverid = message.server.id
      players[serverid].resume()
      await client.send_message(message.channel, "Player resumed")
  if message.content.startswith('m.play '):
      author = message.author
      name = message.content.replace("m.play ", '')                 
      fullcontent = ('http://www.youtube.com/results?search_query=' + name)
      text = requests.get(fullcontent).text
      soup = bs4.BeautifulSoup(text, 'html.parser')
      img = soup.find_all('img')
      div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
      a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
      title = (a[0]['title'])
      a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
      url = ('http://www.youtube.com'+a0['href'])
      delmsg = await client.send_message(message.channel, 'Now Playing ** >> ' + title + '**')
      server = message.server
      voice_client = client.voice_client_in(server)
      player = await voice_client.create_ytdl_player(url)
      players[server.id] = player
      print("User: {} From Server: {} is playing {}".format(author, server, title))
      player.start()
  await client.process_commands(message)
	
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
