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

class Error_handling(commands.Cog):
  def __init__(self, client):
  	self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Error handling module loaded')
    
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    global current_day
    global current_time
    if isinstance(error, commands.CommandNotFound):
      print("\n User used unspecified command: \" {} \" used \'{}\' on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.content, ctx.message.channel, ctx.message.guild, current_time, current_day))
      await ctx.send('``Komenda nie rozpoznana, użyj *$help* w celu uzyskania pomocy.``')
    
    
def setup(client):
  client.add_cog(Error_handling(client))
