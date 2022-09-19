import os, psycopg2, json, re

# - Import database extensions -
from psycopg2.extensions import AsIs, quote_ident
from psycopg2.extras import Json

# - Class connection used for creating multiple connections ( now not supported TODO ) -
class Connection:
	def __init__(self):
		self.connection = self.__connect();
		self.cursor = self.__gen_cursor();
		
	# - Create connection based on Enviroment Variable 'DATABASE_URL' and return it to save as connection -
	def __connect(self):
		url = os.environ.get('DATABASE_URL');
		con = psycopg2.connect(url, sslmode='require');
		return con;
	
	# - Generate cursor for querries generation base on connection generated earlier -
	def __gen_cursor(self):
		con = self.connection;
		cur = con.cursor();
		return cur;
	
	# - In case of long database connection it can expire, code here revokes cursor TODO: Finish code here -
	def __revoke_cursor(self):
		return False;
	
# - Database object, inherit of Connection, handles querries -
class Database(Connection):
	def __init__(self, client):
		super().__init__(); # - Assign Escape and Decode class to handle adapting/decoding of strings, dictionaries etc. to use with dots and better readibility -
		self.client = client
		self.predefined = Predefined(self)
	
	def delete(self, table, condition):
		con = self.connection;
		cur = self.cursor;
		cond_key = list(condition.keys())[0];
		condition = list(condition.values())[0];
		cur.execute(
			"""
			DELETE FROM %s
			WHERE %s = %s;
			""", (AsIs(table), AsIs(cond_key), condition)
		);
		con.commit();
		
	# - Insert variables to new record in given table -
	def insert(self, table, payload):
		con = self.connection; # - use same cursor and connection from class object. -
		cur = self.cursor;
		columns = list(payload.keys()); # - Devide payload for columns and values as given. -
		values = [payload[column] for column in columns];
		for i in range(len(values)):
			if isinstance(values[i], list):
				values[i] = ",".join(str(v) for v in values[i]);
			elif isinstance(values[i], dict):
				values[i] = Json(values[i]);
		#print(values);
		#values = self.escape.all(values);
		#print(values);
		#values = self.escape.wrap(values);
		#values = self.adapt.values(values);
		#values = ",".join("'"+ v + "'" if type(v) is str else str(v) for v in values);
		#print(values);
		#values = self.escape.string(values);
		#print(values);
		match len(values):
			case 1:
				cur.execute( # - Build and execute SQL querry with table, columns, values. -
					"""
					INSERT INTO %s (%s)
					VALUES (%s);
					""", (AsIs(table), AsIs(columns[0]), values[0])
				);
			case 2:
				cur.execute( # - Build and execute SQL querry with table, columns, values. -
					"""
					INSERT INTO %s (%s, %s)
					VALUES (%s, %s);
					""", (AsIs(table), AsIs(columns[0]), AsIs(columns[1]), values[0], values[1])
				);
			case 3:
				cur.execute( # - Build and execute SQL querry with table, columns, values. -
					"""
					INSERT INTO %s (%s, %s, %s)
					VALUES (%s, %s, %s);
					""", (AsIs(table), AsIs(columns[0]), AsIs(columns[1]), AsIs(columns[2]), values[0], values[1], values[2])
				);
			case 4:
				cur.execute( # - Build and execute SQL querry with table, columns, values. -
					"""
					INSERT INTO %s (%s, %s, %s, %s)
					VALUES (%s, %s, %s, %s);
					""", (AsIs(table), AsIs(columns[0]), AsIs(columns[1]), AsIs(columns[2]), AsIs(columns[3]), values[0], values[1], values[2], values[3])
				);
			case 5:
				cur.execute( # - Build and execute SQL querry with table, columns, values. -
					"""
					INSERT INTO %s (%s, %s, %s, %s, %s)
					VALUES (%s, %s, %s, %s, %s);
					""", (AsIs(table), AsIs(columns[0]), AsIs(columns[1]), AsIs(columns[2]), AsIs(columns[3]), AsIs(columns[4]), values[0], values[1], values[2], values[3], values[4])
				);
			case _:
				return 0   # 0 is the default case if x is not found
		"""
		cur.execute( # - Build and execute SQL querry with table, columns, values. -
			"#""
			#INSERT INTO %s (%s)
			#VALUES (%s);
			"#"", (AsIs(table), AsIs(','.join(column for column in columns)), AsIs(values))
		);
		"""
		con.commit(); # - Commit changes to database. -
	
	# - Updates records with given payload and on specified condition, querry affecting every record must be given in condition -
	def update(self, table, payload, condition): 
		con = self.connection; # - use same cursor and connection from class object. -
		cur = self.cursor;
		columns = list(payload.keys()); # - Devide payload for columns and values as given. -
		values = [payload[column] for column in columns];
		#print(f"LEN VALUES IN UPDATE: {len(values)}")
		for i in range(len(values)):
			if isinstance(values[i], list):
				values[i] = ",".join(str(v) for v in values[i]);
			elif isinstance(values[i], dict):
				values[i] = Json(values[i]);
		#values = json.dumps(values, indent = 4)
		cond_key = list(condition.keys())[0];
		condition = list(condition.values())[0];
		#print(f"condition IN UPDATE: {cond_key} == {condition}")
		#print(f"columns IN UPDATE: {columns} inputting value: {values}")
		cur.execute(
			"""
			UPDATE %s
			SET %s = %s
			WHERE %s = %s;
			""", (AsIs(table), AsIs(columns[0] if len(columns) == 1 else tuple(columns)), AsIs(values[0] if len(values) == 1 else tuple(values)), AsIs(cond_key), AsIs(condition)) # AsIs(','.join(columns))
		);
		con.commit();
	# - Function allowing to fetch rows ( and data they contain ) with condition -
	def select(self, table, condition = 1, columns = []): 
		con = self.connection;
		cur = self.cursor;
		if condition == 1: # - Preparing condition, if none given use 1=1 for every record -
			cond_key = condition = 1;
		else:
			cond_key = list(condition.keys())[0];
			condition = list(condition.values())[0];
		if len(columns) == 0: # - Selector used for columns to return, if none given use * for all columns -
			selector = '*';
		elif len(columns) == 1:
			selector = columns[0];
		else:
			selector = tuple(columns);
		cur.execute(
			"""
			SELECT %s FROM %s
			WHERE %s = %s
			""", (AsIs(selector), AsIs(table), AsIs(cond_key), condition)
		); # - Build querry withut any joins -
		records = cur.fetchall() # - Get every record in return -
		con.commit()
		if len(records) == 1: # - Make return records value more easy for later use, get rid of un-needed lists -
			records = records[0];
			if len(records) == 1:
				records = records[0]; # - If in return was only one record with single value make returned value this value -
		else:
			r = [];
			for record in records:
				if len(record) == 1: # - In case of multiple rows return check if any of them is made out of single value, then shorten -
					r.append(record);
				else:
					r.append(record);
			records = r;
		return records;
	
class Predefined(Database):
	def __init__(self, database):
		self.database = database
		
	def add_new_guild(self, guild):
		roles = {};
		for r in guild.roles:
			if r != guild.default_role and not r.managed:
				roles[r.id] = r.name;
		payload = { "id": guild.id,
			"prefix": self.database.client.configuration.read(category="utilities", key="database.defaults.prefix"),
			"language": self.database.client.configuration.read(category="utilities", key="database.defaults.language"),
			"roles": roles
		};
		self.database.insert(table = 'guilds.properties', payload = payload);
		
	def remove_guild(self, guild):
		self.database.delete(table = 'guilds.properties',
					    condition = {"id": guild.id});

	def update_roles(self, guild, roles):
		self.client.database.update(
			table = 'guilds.properties', 
			payload = {"roles": roles}, 
			condition = {"id": guild.id}
		);
