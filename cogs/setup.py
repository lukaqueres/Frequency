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

from functions import get_prefix, get_time

load_dotenv()

class Setup(commands.Cog):
  def __init__(self, client):
  	self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Setup module loaded')

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    print("\n Bot joined in guild: \" {} \" guild on \" {} \".".format(guild, get_time()))
    with open('data.json', 'r') as f:
      prefixes = json.load(f)
      
      prefixes[str(guild.id)] = '$'
    
    with open('data.json','w') as f:
      json.dump(prefixes, f, indent=4)
      
  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    print("\n Bot removed from guild: \" {} \" guild on \" {} \".".format(guild, get_time()))
    with open('data.json', 'r') as f:
      prefixes = json.load(f) 
      
      prefixes.pop(str(guild.id))
    
    with open('data.json','w') as f:
      json.dump(prefixes, f, indent=4)
    
  @commands.command()
  @has_permissions(manage_messages=True)
  async def prefix_change(self, ctx, prefix):
    await ctx.send(f'Zmieniono prefix komend na ``{prefix}``')
    print("\n Prefix changed in guild: \" {} \" guild to \"{}\" on \" {} \".".format(ctx.message.guild, prefix, get_time()))
    with open('data.json', 'r') as f:
      prefixes = json.load(f)
      
      prefixes[str(ctx.message.guild.id)] = prefix
    
    with open('data.json','w') as f:
      json.dump(prefixes, f, indent=4)
    
def setup(client):
  client.add_cog(Setup(client))
