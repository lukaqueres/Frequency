import os, psycopg2, json

# - Import database extensions -
from psycopg2.extensions import AsIs

# - Class connection used for creating multiple connections ( now not supported TODO ) -
class Connection:
	def __init__(self):
		self.connection = self.__connect();
		self.cursor = self.__gen_cursor();
		
	# - Create connection based on Enviroment Variable 'DATABASE_URL' and return it to save as connection -
	def __connect(self):
		connection = os.environ.get('DATABASE_URL');
		con = psycopg2.connect(connection);
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
	def __init__(self):
		super().__init__();
		self.adapt = Adapt(); # - Assign Adapt and Decode class to handle adapting/decoding of strings, dictionaries etc. to use with dots and better readibility -
		self.decode = Decode();
	
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
		for value in values: # - Check for types not supported and change to more supported ones. Currently working json as dictionary. TODO: Test for more types. -
			if isinstance(value, dict):
				toEscapeKeys = list(value.keys());
				toEscapeValues = list(value.values());
				escapedKeys = [];
				escapedValues = [];
				escapedDict = {};
				for k in toEscapeKeys:
					escapedKeys.append(self.adapt.escape(k));
				for v in toEscapeValues:
					escapedValues.append(self.adapt.escape(v));
				for i in range(len(escapedKeys)):
    					escapedDict[escapedKeys[i]] = escapedValues[i]
				values[values.index(value)] = json.dumps(escapedDict, indent = 4);
			elif type(value) is str:
				values[values.index(value)] = self.adapt.escape(value);
			else:
				pass;
		print(values);
		#values = self.adapt.values(values);
		values = ",".join("'"+ v + "'" if type(v) is str else str(v) for v in values);
		print(values);
		cur.execute( # - Build and execute SQL querry with table, columns, values. -
			"""
			INSERT INTO %s (%s)
			VALUES (%s);
			""", (AsIs(table), AsIs(','.join(column for column in columns)), AsIs(values))
		);
		con.commit(); # - Commit changes to database. -
	
	# - Updates records with given payload and on specified condition, querry affecting every record must be given in condition -
	def update(self, table, payload, condition): 
		con = self.connection;
		cur = self.cursor;
		columns = list(payload.keys());
		values = [payload[column] for column in columns];
		
		for value in values:
			if isinstance(value, dict):
				toEscapeKeys = list(value.keys());
				toEscapeValues = list(value.values());
				escapedKeys = [];
				escapedValues = [];
				escapedDict = {};
				for k in toEscapeKeys:
					escapedKeys.append(self.adapt.escape(k));
				for v in toEscapeValues:
					escapedValues.append(self.adapt.escape(k));
				for i in range(len(escapedKeys)):
    					escapedDict[escapedKeys[i]] = escapedValues[i]
				values[values.index(value)] = json.dumps(escapedDict, indent = 4);
			if type(value) is str:
				values[values.index(value)] = self.adapt.escape(value);
		values = json.dumps(values, indent = 4)
		cond_key = list(condition.keys())[0];
		condition = list(condition.values())[0];
		cur.execute(
			"""
			UPDATE %s
			SET %s = %s
			WHERE %s = %s;
			""", (AsIs(table), AsIs(columns[0] if len(columns) == 1 else tuple(columns)), values, AsIs(cond_key), condition) # AsIs(','.join(columns))
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
	
class Adapt():
	def __find(string, tofind):
		indexes = [];
		if len(tofind) == 1:
			for i in range(len(string)):
				if string[i] == tofind:
					indexes.append(i);
		return indexes;
	
	def __swap(s, newstring, index, nofail=False):
		# raise an error if index is outside of the string
		if not nofail and index not in range(len(s)):
			raise ValueError("index outside given string")
		print(index);
		# if not erroring, but the index is still not in the correct range..
		if index < 0:  # add it to the beginning
			return newstring + s
		if index > len(s):  # add it to the end
			return s + newstring

		# insert the new string between "slices" of the original
		return s[:index] + newstring + s[index + 1:]
	
	def values(self, values):
		values = ",".join("'"+ v + "'" if type(v) is str else str(v) for v in values);
		return values;
	
	def string(self, string):
		string = string.replace('"', '""');
		return string;
	
	def dictionary(self, dictionary):
		dictionary = json.dumps(dictionary);
		return dictionary;
	
	def escape(self, string):
		if type(string) is str:
			indexes = self.__find(string,"'")
			for i in indexes:
				if string[i-1] == '/':
					pass;
				else:
					string = self.__swap(string, "\'", int(i))
			indexes = self.__find(string,'"')
			for i in indexes:
				if string[i-1] == '/':
					pass;
				else:
					string = self.__swap(string, '\"', int(i))
		return string;
			
	def wrap(self, value):
		pass;
	
class Decode():
	def string(self, string):
		string = string.replace('""', '"');
		return string;
	
	
