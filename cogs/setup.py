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

class Setup(commands.Cog):
  def __init__(self, client):
  	self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Setup module loaded')

    
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
      
  @commands.command()
  async def help(self, ctx):
    message = ctx.message
    embed=discord.Embed(title="Help", description="Pomoc - znajdziesz tu listę oraz informacje dotyczące komend których możesz użyć na tym serwerze", color=0x0000ff)
    embed.add_field(name="$join", value="Dołącza do kanału na którym znajduje się użytkownik.", inline=False)
    embed.add_field(name="$play [ url / słowa kluczowe ]", value="Odtwarza muzykę na kanale głosowym na podstawie adresu url, lub słów kluczowych. Wymaga aby użytkownik znajdował się na kanale głosowym.", inline=False)
    embed.add_field(name="$stop", value="Zatrzymuje odtwarzanie oraz wychodzi z kanału głosowego.", inline=True)
    embed.add_field(name="$volume [ liczba ]", value="Zmienia głośność odtwarzania muzyki na kanale głosowym na określony procent ( domyślnie 50% ).", inline=True)
    if (message.author.guild_permissions.manage_messages):
      embed.add_field(name="Zarządzanie wiadomościami", value="Dostępne jedynie dla użytkowników z uprawnieniem zarządzania wiadomościami.", inline=False)
      embed.add_field(name="$clear [ liczba ]", value="Usuwa określoną liczbę wiadomości z kanału ( nie licząc wiadomości z komendą ).", inline=True)
    if (message.author.guild_permissions.ban_members):
      embed.add_field(name="Zarządzanie użytkownikami", value="Dostępne jedynie dla użytkowników z odpowiednimi uprawnieniami.", inline=False)
      embed.add_field(name="$ban [ użytkownik ]", value="Nakłada bana na użytkownika.", inline=True)
      embed.add_field(name="$unban [ użytkownik ]", value="Usuwa bana z użytkownika, jeżeli go posiada.", inline=True)
    if (message.author.guild_permissions.administrator):
      embed.add_field(name="Zarządzanie serwerem", value="Dostępne jedynie dla użytkowników z uprawnieniami administratora.", inline=False)
      embed.add_field(name="$prefix_change [ prefix]", value="Zmienia prefiks serwera z którego korzysta bot. **UWAGA** działa jedynie przez krótki okres.", inline=False)
    msg = await ctx.send(embed=embed)
    #await msg.add_reaction(':ballot_box_with_check:')
    
#
#<----------> 'set' command - set channels and some settings <------------------------------------------------------------------------>
#

  @commands.command()
  async def set(self, ctx, task = 'default', value = 'default'):
    guild = ctx.guild
    guild_id = guild.id
    value_length = len(value)
    if (task == 'prefix'): #>-------------------------------------------< Task - prefix
      if (value == 'default'): # If value wasn't changed
        await ctx.send("You must specify new prefix!")
        return 0
      elif (value_length > 2): # If value is too long
        await ctx.send("New prefix length must be long 2 characters max!")
        return 0
      else: # If value seems legit
        cur.execute("UPDATE servers_properties SET guild_prefix = '{}' WHERE guild_id = '{}';".format(value, guild_id))
        con.commit()
        await ctx.send("This guild prefix changed for: '{}'.".format( value ))
        
    
def setup(client):
  client.add_cog(Setup(client))
