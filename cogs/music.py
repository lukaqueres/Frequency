import discord, json, io, os, typing, requests, random, asyncio, youtube_dl
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

from functions import get_prefix, get_time

#client = commands.Bot(command_prefix = get_prefix)
client = discord.client
load_dotenv()
players = {}
voice_clients = {}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Music module loaded')
          
  @commands.command()
  async def play(self, ctx, query): #async def play(self, ctx, url : str, query):
    url = query
    print("\n User used play command: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, get_time()))
    guild = ctx.message.author.guild
    voice_state = ctx.author.voice
    guild = ctx.message.guild
    channel = ctx.message.author.voice.channel

    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)

    voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
    if not ctx.message.author.voice:
      await ctx.send("``Musisz się znajdować na kanale głosowym``")
      return
    else:
      channel = ctx.message.author.voice.channel
      await channel.connect()
      await ctx.send(f'Połączono z ``{channel}``')
    voice_channel = ctx.message.author.voice.channel
    
    YTDL_OPTIONS = {'noplaylist': 'True'}  #YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
      'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)
    with YoutubeDL(YTDL_OPTIONS) as ytdl:
      URL = ytdl.extract_info(url, download=False)
    #player = client.voice_clients[0]
    #players[guild.id] = player
    #player.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    #ctx.voice_client.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

    await ctx.send(f'Now playing: {player.title}')

    
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
    
