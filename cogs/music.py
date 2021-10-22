import discord, json, io, os, typing, requests, random, asyncio
from os import getenv
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel
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
  
    voice_channel = ctx.author.voice.channel
    voice = get(self.bot.voice_clients, guild=ctx.guild) 
    guild = ctx.message.guild
    voice_client = guild.voice_client
    #await voice_channel.connect()
    if voice and voice.is_connected():
      await voice.move_to(voice_channel)
    else:
      voice = await voice_channel.connect()
  
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
      'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    #voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
      with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
      URL = info['url']
      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
      voice.is_playing()
      #check if the bot is already playing
    else:
      await ctx.send("Bot już gra")
    
  @commands.command()
  async def leave(self, ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send('"Bot nie jest połączony z żadnym kanałem głosowym."')
  
  @commands.command()
  async def pause(self, ctx):
      voice = discord.utils.get(client.voice_clients, guild=ctx.guild) #ctx.guild.voice_channels
      if voice.is_playing():
          voice.pause()
      else:
          await ctx.send('"Obecnie nic nie jest odtwarzane."')


  @commands.command()
  async def resume(self, ctx):
      voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
      if voice.is_paused():
          voice.resume()
      else:
          await ctx.send('"Obecnie nic nie jest zatrzymane."')

  @commands.command()
  async def stop(self, ctx):
      voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
      voice.stop()
    
def setup(client):
  client.add_cog(Music(client))
    
