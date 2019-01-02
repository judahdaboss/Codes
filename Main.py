
import discord
from discord.ext import commands
import asyncio
import requests, bs4
from itertools import cycle
import os
import time
import youtube_dl
from discord import opus

client = commands.Bot(command_prefix=("b!"))
client.remove_command("help")
status = ["testing the bot", "b!help", "created by noobperson"]

async def change_status():
	await client.wait_until_ready()
	msgs = cycle(status)
	
	while not client.is_closed:
		current_status = next(msgs)
		await client.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(5)

players = {}	

@client.event 
async def on_ready():
	print('Logged in as')
	print("User name:", client.user.name)
	print("User id:", client.user.id)
	print('---------------')
	
@client.event
async def on_message(message):
  if message.content == 'b!stop':
      serverid = message.server.id
      players[serverid].stop()
  if message.content == 'b!pause':
      serverid = message.server.id
      players[serverid].pause()
      await client.send_message(message.channel, "Player paused")
  if message.content == 'b!resume':
      serverid = message.server.id
      players[serverid].resume()
      await client.send_message(message.channel, "Player resumed")
  if message.content.startswith('b!play '):
      author = message.author
      name = message.content.replace("b!play ", '')                 
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

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="b!ping", description="get bot's response time", color=0xFFFFF)
    embed.add_field(name="b!join", value="join voice channel first and then try b!join")
    embed.add_field(name="b!leave", value="to make the bot leave voice channel")
    embed.add_field(name="b!play", value="play music from the bot")
    embed.add_field(name="b!stop", value="to stop the music")
    embed.add_field(name="b!pause", value="to pause the music")
    embed.add_field(name="b!resume", value="to resume the music")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def ping(ctx):
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await client.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)
    
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    await client.say('Connected to voice channel: **[' + str(channel) + ']**')
	
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await client.say('Left voice channel')
	
client.loop.create_task(change_status())
client.run(os.environ['BOT_TOKEN'])
