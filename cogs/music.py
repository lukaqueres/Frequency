import discord, json, io, os, typing, requests, random, asyncio, pafy
from os import getenv
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel, PCMVolumeTransformer
from discord.ext import tasks, commands
from discord.utils import get
from youtube_dl import *
from discord.ext.commands import has_permissions, MissingPermissions, bot

now = datetime.now() + timedelta(hours=2)
today = date.today()
current_day = today.strftime("%d/%m/%Y")   #global current_day
current_time = now.strftime("%H:%M:%S")    #global current_time
client = discord.Client()
load_dotenv()
players = {}

class Music(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Music module loaded')
          
  @commands.command()
  async def play(self, ctx, url : str):
    global current_day
    global current_time
    print("\n User used play command: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, current_time, current_day))
    guild = ctx.message.author.guild
    voice_state = ctx.author.voice
    guild = ctx.message.guild
    voice_client = guild.voice_client
    if not ctx.message.author.voice:
      await ctx.send("``Musisz się znajdować na kanale głosowym``")
      return
    else:
      channel = ctx.message.author.voice.channel
      await channel.connect()
      await ctx.send(f'Połączono z ``{channel}``')
    voice_channel = ctx.message.author.voice.channel
    
  
    YDL_OPTIONS = {'noplaylist': 'True'} #YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
      'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)
    with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
    URL = info['url']
    player = bot.voice_clients[0]
    players[guild.id] = player
    player.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    """if not voice_channel.is_playing():
      with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
      URL = info['url']
      voice_channel.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
      voice_channel.is_playing()
      #check if the bot is already playing
    else:
      await ctx.send("Bot już gra")"""
    
  @commands.command()
  async def leave(self, ctx):
    voice_channel = ctx.message.author.voice.channel
    if voice.is_connected():
        await voice_channel.disconnect()
    else:
        await ctx.send('"Bot nie jest połączony z żadnym kanałem głosowym."')
  
  @commands.command()
  async def pause(self, ctx):
    voice_channel = ctx.message.author.voice.channel
    if voice_channel.is_playing():
      voice_channel.pause()
    else:
      await ctx.send('"Obecnie nic nie jest odtwarzane."')


  @commands.command()
  async def resume(self, ctx):
    voice_channel = ctx.message.author.voice.channel
    if voice_channel.is_paused():
      voice_channel.resume()
    else:
      await ctx.send('"Obecnie nic nie jest zatrzymane."')

  @commands.command()
  async def stop(self, ctx):
    voice_channel = ctx.message.author.voice.channel
    async def stop(self, ctx):
      voice_channel.stop()
    
def setup(client):
  client.add_cog(Music(client))
    
