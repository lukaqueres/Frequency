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

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

class Database_maintenance(commands.Cog):
  def __init__(self, client):
  	self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Database maintenance module loaded')
    
#
#<----------> On Bot join to guild <----------------------------------------------------------------->
#
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    print("\n Bot joined in guild: \" {} \" guild on \" {} \".".format(guild, get_time()))
    default_prefix = '$'
    date_of_join = str("{") + get_time("DD") + str("}")
    cur.execute("INSERT INTO SERVERS_PROPERTIES ( GUILD_ID, GUILD_NAME, DATE_OF_JOIN, GUILD_PREFIX, NUMBER_OF_USERS, ANTY_SPAM_FEATURE, ECONOMY, MUSIC, UPDATES) VALUES ('{}', '{}', '/{{}/}', '{}', '{}', '{}', '{}', '{}', '{}')".format(guild.id, guild.name, date_of_join, default_prefix, guild.member_count, "NO", "NO", "YES", "NO"));
    con.commit()
#
#<----------> On Bot remove from guild <----------------------------------------------------------------->
#
  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    print("\n Bot removed from guild: \" {} \" guild on \" {} \".".format(guild, get_time()))
    with open('data.json', 'r') as f:
      prefixes = json.load(f) 
      
      prefixes.pop(str(guild.id))
    
    with open('data.json','w') as f:
      json.dump(prefixes, f, indent=4)
    
def setup(client):
  client.add_cog(Database_maintenance(client))
