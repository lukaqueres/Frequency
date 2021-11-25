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

class Management(commands.Cog):
  def __init__(self, client):
  	self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Management module loaded')
    
  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    print("Member {member} banned on {ctx.guild} guild on {get_time()} ."

  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
      user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
          await ctx.guild.unban(user)
          print("Member {member} unbanned on {ctx.guild} guild on {get_time()} ."
          await ctx.send(f'Unbanned {user.mention}')
          return
    
def setup(client):
  client.add_cog(Management(client))
