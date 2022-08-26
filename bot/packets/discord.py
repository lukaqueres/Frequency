import json, os

# - Import database in case of error -
from packets.database import Database

def prefix(client, message):
	with open('./configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting logging details. -
		configuration = json.load(c); 
		log = configuration['developer']['log'];
		defaults = configuration['values']['defaults'];
	try:
		database = Database(); # - TODO: Check how to get database object from bot.py main file, for now this will do -
		properties = database.select(table = 'guilds', 
			columns = ['properties'],
			condition = {"id": message.guild.id}
			);
		prefix = properties['prefix'];
	except Exception as e:
		if log['exceptions']:
			prefix = defaults['prefix'];
			print(f'Error while getting prefix: {getattr(e, "message", repr(e))}');
	return prefix;
