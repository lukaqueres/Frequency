import json, os

# - Import database in case of error -
from packets.database import Database

def prefix(client, message):
	database = Database; # - TODO: Check hov to get database object from bot.py main file, for now this will do -
	properties = database.select(table = 'guilds', 
			columns = ['properties'],
			condition = message.guild.id 
			);
	prefix = properties['prefix'];
	return prefix;
