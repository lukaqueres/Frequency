import json, os

def prefix(client, message):
	connection = os.environ.get('DATABASE_URL');
	con = psycopg2.connect(connection);
	cur = con.cursor()
	cur.execute(
		"SELECT cmdPrefix FROM SERVERS_PROPERTIES WHERE guild_id=%s",
		(message.guild.id, )
	)
	row = cur.fetchone()
	prefix = row[0]
	con.commit()
	#print("Prefix downloaded succesfully as '{}' on '{}' guild.".format(prefix, message.guild))
	return prefix
