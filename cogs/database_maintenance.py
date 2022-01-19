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

client = commands.Bot

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

global check_database_on_startup
check_database_on_startup = 'TRUE'

#
#<----------> Check database <------------------------------------------------------------------------>
#

def check_database():
  print('Database check start:')
  print('Checking guilds: {} '.format( client.guilds ))
  guilds_id = []
  default_prefix = '$'
  default_language = 'ENG'
  date_of_join = str("{") + get_time("DD") + str("}")
  for guild in client.guilds:
    members_count = len([m for m in guild.members if not m.bot]) # doesn't include bots 
    guilds_id.append(guild.id)
    print('Database Check: Guild {} check.'.format( guild ))
    cur.execute("""IF NOT EXISTS ( SELECT 1 FROM servers_properties WHERE guild_id = {} ) 
                   INSERT INTO SERVERS_PROPERTIES ( GUILD_ID, GUILD_NAME, DATE_OF_JOIN, GUILD_PREFIX, NUMBER_OF_USERS, ANTY_SPAM_FEATURE, ECONOMY, MUSIC, UPDATES, NUMBER_OF_MEMBERS, GUILD_LANGUAGE) 
                   VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
                   IF EXISTS ( SELECT 1 FROM servers_properties WHERE guild_id = {} ) 
                   INSERT INTO SERVERS_PROPERTIES ( NUMBER_OF_USERS, NUMBER_OF_MEMBERS, GUILD_LANGUAGE) WHERE guild_id = {}
                   VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format( guild.id, guild.id, guild.name, date_of_join, default_prefix, guild.member_count, "NO", "NO", "YES", "NO", members_count, default_language, guild.id, guild.id, members_count, guild.member_count, default_language ));
    con.commit()

if check_database_on_startup == 'TRUE':
  check_database()
#
#<=========> Cog start <===============================================================================>
#

class Database_maintenance(commands.Cog):
  def __init__(self, client):
  	self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Database maintenance module loaded')
    
#
#<----------> On Bot join to guild <-------------------------------------------------------------------->
#
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    print("\n Bot joined in guild: \" {} \" guild on \" {} \".".format(guild, get_time()))
    default_prefix = '$'
    default_language = 'ENG'
    members_count = len([m for m in guild.members if not m.bot]) # doesn't include bots
    date_of_join = str("{") + get_time("DD") + str("}")
    cur.execute("SET datestyle = dmy; INSERT INTO SERVERS_PROPERTIES ( GUILD_ID, GUILD_NAME, DATE_OF_JOIN, GUILD_PREFIX, NUMBER_OF_USERS, ANTY_SPAM_FEATURE, ECONOMY, MUSIC, UPDATES, NUMBER_OF_MEMBERS, GUILD_LANGUAGE) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(guild.id, guild.name, date_of_join, default_prefix, guild.member_count, "NO", "NO", "YES", "NO", members_count, default_language));
    con.commit()
#
#<----------> On Bot remove from guild <----------------------------------------------------------------->
#
  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    print("\n Bot removed from guild: \" {} \" guild on \" {} \".".format(guild, get_time()))
    sql = "DELETE FROM SERVERS_PROPERTIES WHERE GUILD_ID = %s"
    guild = (guild.id, )
    cur.execute(sql, guild)
    con.commit()
    
#
#<----------> On User join to guild <-------------------------------------------------------------------->
#
  @commands.Cog.listener()
  async def on_member_join(self, member):
    guild = member.guild.id
    members_count = len([m for m in member.guild.members if not m.bot]) # doesn't include bots
    #print("\n Member joined: \" {} \" guild on \" {} \".".format(member.guild.name, get_time()))
    cur.execute("SET datestyle = dmy; UPDATE SERVERS_PROPERTIES SET (NUMBER_OF_USERS, NUMBER_OF_MEMBERS) = ('{}', '{}') WHERE GUILD_ID = '{}'".format(members_count, member.guild.member_count, guild))
    con.commit()

#
#<----------> On User leave from guild <----------------------------------------------------------------->
#
  @commands.Cog.listener()
  async def on_member_remove(self, member):
    guild = member.guild.id
    members_count = len([m for m in member.guild.members if not m.bot]) # doesn't include bots
    #print("\n Member left: \" {} \" guild on \" {} \".".format(member.guild.name, get_time()))
    cur.execute("SET datestyle = dmy; UPDATE SERVERS_PROPERTIES SET (NUMBER_OF_USERS, NUMBER_OF_MEMBERS) = ('{}', '{}') WHERE GUILD_ID = '{}'".format(members_count, member.guild.member_count, guild))
    con.commit()

    
def setup(client):
  client.add_cog(Database_maintenance(client))
