import json, os

# - Import database in case of error -
from packets.database import Database

def prefix(client, message):
	global database;
	properties = database.select(table = 'guilds', 
			columns = ['properties'],
			condition = message.guild.id 
			);
	prefix = properties['prefix'];
	return prefix;
