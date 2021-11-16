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

from functions import get_prefix

now = datetime.now() + timedelta(hours=2)
today = date.today()
current_day = today.strftime("%d/%m/%Y")   #global current_day
current_time = now.strftime("%H:%M:%S")    #global current_time
client = commands.Bot(command_prefix = get_prefix)

load_dotenv()

class Spam_detection(commands.Cog):
  def __init__(self, client):
  	self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Spam detection module loaded')
    
  @commands.Cog.listener()
  async def on_message(self, message):
    #await client.process_commands(message)
    global current_day
    global current_time
    black_listed = ['Free', 'free', 'Nitro', 'nitro', 'Discord', 'discord', 'giveaway', 'Giveaway', 'Skin', 'skin', 'CS:GO', 'Counter-Strike: Global Offensive', 'CS']
    black_listed_length = (len(black_listed))
    black_listed_words_number_detected = 0
    if (message.author == client.user):
      return
    if (('http' in message.content ) or ('https' in message.content)):
      for x in black_listed:
        if (x in message.content):
          black_listed_words_number_detected += 1
          if (black_listed_words_number_detected == 2):
            print("\nPosible scam by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(message.author, message.channel, message.guild, get_time()))
            embed = discord.Embed(
              title="Możliwy scam",
              description=" ",
              color=0x0000ff,
            )
            embed.add_field(name="Użytkownik:", value=message.author, inline=True),
            embed.add_field(name="Serwer:", value=message.guild, inline=True),
            embed.add_field(name = chr(173), value = chr(173))
            embed.add_field(name="Data:", value=current_day, inline=True),
            embed.add_field(name="Godzina:", value=current_time, inline=True),
            embed.add_field(name = chr(173), value = chr(173))
            embed.add_field(name="Treść wiadomości:", value=message.content, inline=False),
            #user = await client.fetch_user("429949201254842369")
            author = message.author
            role = discord.utils.get(author.guild.roles, name="🤐 Wyciszony")
            RDPchannel = client.get_channel(887604610972409906)
            RDPguild = client.get_guild(640181649463705650)
            if role in message.author.roles:
              await message.delete()
            else:
              await message.delete()
              #await DMChannel.send(user, embed=embed)
              #await client.add_roles(author, role)
              if message.guild == RDPguild:
                await RDPchannel.send(embed=embed)
    else: 
      return
    
def setup(client):
  client.add_cog(Spam_detection(client))
