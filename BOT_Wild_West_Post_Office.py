import discord, json, io, os, typing, requests, random, asyncio, psycopg2, nltk
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
#from youtube_dl import YoutubeDL
from functions import get_prefix, get_time

try:
	DATABASE_URL = os.environ.get('DATABASE_URL')
	con = psycopg2.connect(DATABASE_URL)
	cur = con.cursor()
	print("Bot database opened successfully")
except:
	print("Failed to open database")

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = get_prefix, intents=intents)

now = datetime.now() + timedelta(hours=2)
today = date.today()
current_day = today.strftime("%d/%m/%Y")   #global current_day
current_time = now.strftime("%H:%M:%S")    #global current_time

client.remove_command('help')

@client.event #---------------------------------READY---------------------------------------------------------------------------------------------------------
async def on_ready():
	await client.change_presence(status=discord.Status.online, activity=discord.Game('Red Dead Redemption 2'))          #status online/offline  , activity=discord.Game('Red Dead Redemption 2')
	print('Bot logged in with:')
  
async def status_change():
	await client.wait_until_ready()
	statuses = ["Red Dead Redemption 2", "Red Dead Redemption 1", "Red Dead Online", "Red Dead Revolver" ]
	while not client.is_closed():
    		sleep_time = random.randint(1800,3600)
    		status = random.choice(statuses)
    		await client.change_presence(status=discord.Status.online, activity=discord.Game(name=status))
    		print("Activity has been changed to: {}, and next change will be again after: {} seconds." .format(status, sleep_time))
    		await asyncio.sleep(sleep_time)
	client.loop.create_task(status_change())

#----------------------------------------------------------------------------------------COMMANDS-------------------------------------------------------------------------------------------------------------
load_dotenv()
players = {}
            
@client.command()
@has_permissions(manage_messages=True)
async def cytaty(ctx):
    	print(" \nCytaty command has been used by member on:")
    	channel  = ctx
    	embed = discord.Embed(
        	title="Czasy rewolwerowców i bandytów dobiegły końca. \nDziki zachód stał się legendą, a za istnieniem legend zawsze kryją się niezapomniane słowa. Aby je poznać musisz skorzystać ze zwoju na poczcie",
        	description="   Po naciśnięciu reakcji, zostanie wysłany jeden z wielu cytatów z gier: \n   Red Dead Redemption, Red Dead Redemption 2 oraz Red Dead Online",
        	color=0x0000ff,
        )
    	amount = 1
    	await ctx.channel.purge(limit = amount)
    	msg = await ctx.send(embed=embed)
    	await msg.add_reaction('📜')
    	#await msg.add_reaction('🏷️')
    	#await ctx.message.add_reaction('📜')                                                    Emoji do wysłanej wiadomości przez użytkownika
    	#await ctx.send(' >>> Ta opcja niedługo będzie działać :scroll:')                         Zwykła wiadomość jako cytat

@client.command()
@has_permissions(manage_messages=True)
async def embed(ctx):
    	now = datetime.now()
    	today = date.today()
    	current_day = today.strftime("%d/%m/%Y")
    	current_time = now.strftime("%H:%M:%S")
    	print("\nEmbed has been triggered by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, current_time, current_day))
    	await ctx.channel.purge(limit = 1)
    	embed = discord.Embed(
        	#name="Lukaqueres"
        	title="Nowości & Aktualności Red Dead Online",
        	description=" Co tygodniowa aktualizacja RDO: 07.09.2021 - 13.09.2021",
        	color=0x0000ff,
        	)
    	embed.add_field(name="Zniżki:", value="**-** 5 sztabek na licencję łowcy nagród \n**-** 30% zniżki na broszury ról \n**-** 40% zniżki na konie bretońskie\n**-** 40% zniżki na pasy na broń ról\n**-** 40% na amunicję i strzemiona\n**-** 50% na ostrogi", inline=True)
    	embed.add_field(name="Aktualności", value="W tym tygodniu wydarzenia w grze swobodnej oraz tryb do broni przynosi 2 razy więcej dochodów jak i PD. W trakcie przestępstw krwawej forsy można zdobyć więcej *kapitali* niż zwykle. W tym tygodniu jest również dostępna odzież z poprzednich przepustek bandyty.", inline=True)
    	embed.add_field(name="Witamy 3 odsłonę Klubu Rewolwerowca", value="\nCena wynosi 25 sztabek złota które zwracają się po osiągnęciu 25, maksymalnego poziomu. Możemy w niej zdobyć m. in. Nową kamizelkę, nóż, kurtkę, maskę czy końską grzywę.\nJest dostępna do 4 października 2021 ", inline=False)
    	embed.add_field(name="Więcej", value="""**W tym tygodniu:**\n- Za dowolną modyfikację broni można zarobić 25 nabojów zapalających do strzelby jak i 200 nabojów express do rewolweru\n- Wszyscy gracze RDO którzy zalogują się w tym tygodniu dostaną 3 specjalne oleje z węża i 3 silne serum w ciągu 72 godzin.
                    \n\nPosiadacze 2 poprzednich odsłon Klubu Rewolwerowca którzy zakupią tą (3) odsłonę otrzymają 25 not kapitałowych i 10 darmowych szybkich podróży w ciągu 72 godzin od zakupu. \nPrzypominamy że posiadanie wszystkich 4 odsłon zapewni darmową hallowienową przepustkę.  """, inline=False)
    	embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    	embed.set_thumbnail(url="https://prod.cloud.rockstargames.com/global/Events/23152/171b3f1d-4598-4415-9151-957aa943388a.jpg")
    	embed.set_footer(text="Miłej gry")
    	msg = await ctx.send(embed=embed)
    	await msg.add_reaction('🏷️')

@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, number : int ):
	global current_day
	global current_time
	number = number + 1
	print("\n Clear with walue {} has been triggered by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} \".".format(number, ctx.message.author, ctx.message.channel, ctx.message.guild, get_time()))
	await ctx.channel.purge(limit = number)

@clear.error
async def clear_error(error, ctx):
	if isinstance(error, MissingPermissions):
        	global current_day
        	global current_time
        	print("\n Clear has been triggered and didn't work by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, get_time()))
        	print(" Reason: \" not enough permissions \"")
        	await ctx.channel.purge(limit = 1)







@client.command() 
#@has_permissions(manage_messages=True)
async def ping(ctx):
	await ctx.send(f'Ping: {round(client.latency * 1000)} ms')
	print("Ping: {} ms on guild: {}" .format(round(client.latency * 1000), ctx.message.guild))

#install nltk packages:
packages = { 'averaged_perceptron_tagger', 'wordnet', 'pros_cons', 'reuters', 'hmm_treebank_pos_tagger', 'maxent_treebank_pos_tagger', 'universal_tagset', 'punkt', 'averaged_perceptron_tagger_ru', 'snowball_data', 'rslp', 'porter_test', 'vader_lexicon', 'treebank', 'dependency_treebank', 'stopwords' }
for package in packages:
	nltk.download(package)
	print("{} NLTK package downloaded.".format(package))

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run('ODc1MjcxOTk1NjQ0ODQyMDA0.YRTGkQ.52s28D_CmdNtZm3g4_llDs4AV9E')
