def prefix(client, message):
	con = get_connection()
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
