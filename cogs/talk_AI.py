import discord, json, io, os, typing, requests, random, asyncio, psycopg2
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

intents = discord.Intents.default()
intents.members = True

DATABASE_URL = os.environ.get('DATABASE_URL') 
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

class Talk_AI(commands.Cog):
  def __init__(self, client):
  	self.client = client
	
  @commands.Cog.listener()
  async def on_ready(self):
    print('Database maintenance module loaded')
	
  @commands.Cog.listener()
  async def on_message(self, message):
		
    break
		
def setup(client):
  client.add_cog(Talk_AI(client))
