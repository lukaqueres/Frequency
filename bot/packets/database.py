import os, psycopg2, json, re

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
		self.escape = Escape();
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
				values[values.index(value)] = self.escape.string(value);
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
	def __find(self, string, tofind):
		indexes = [];
		if len(tofind) == 1:
			for i in range(len(string)):
				if string[i] == tofind:
					indexes.append(i);
		return indexes;
	
	def __swap(self, s, newstring, index, nofail=False):
		# raise an error if index is outside of the string
		if not nofail and index not in range(len(s)):
			return s;
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
			#indexes = self.__find(string,"'")
			indexes = [_.start() for _ in re.finditer(string, "'")];
			print(indexes);
			alreadyEscaped = '\\';
			print(alreadyEscaped);
			for i in indexes:
				print(string[i-1] + string[i]);
				if string[i-1] == alreadyEscaped:
					pass;
				else:
					string = self.__swap(string, "\'", int(i))
			#indexes = self.__find(string,'"')
			indexes = [_.start() for _ in re.finditer(string, '"')];
			print(indexes);
			for i in indexes:
				print(string[i-1] + string[i]);
				if string[i-1] == alreadyEscaped:
					pass;
				else:
					string = self.__swap(string, '\"', int(i))
		return string;
			
	def wrap(self, value):
		pass;

class Escape():
	def __input(self, s, newstring, index, nofail=False):
		# raise an error if index is outside of the string
		if not nofail and index not in range(len(s)):
			print(f'Not added {newstring} to the {s}');
			return s;
		# if not erroring, but the index is still not in the correct range..
		if index < 0:  # add it to the beginning
			print(f'Added {newstring} to beggining of {s}');
			return newstring + s
		if index > len(s):  # add it to the end
			print(f'Added {newstring} to end of {s}');
			return s + newstring

		# insert the new string between "slices" of the original
		print(f'Added {newstring} in the middle of {s}');
		return s[:index] + newstring + s[index + 1:]
	
	def __indexes(self, string, lookingFor, start = 0):
		string = string[start:];
		indexes = [str(i) for i, x in enumerate(string, start) if x == lookingFor];
		print(list(enumerate(string, start)));
		return indexes;
		
	def all(self, values):
		pass;
		
	def string(self, string, passEscaped = False):
		elements = {'"': '\\\"', '\'': '\\\''};
		for key, value in elements:
			print(f'key: {key}, value: {value}');
			index = 0;
			nextIndex = self.__indexes(string, key, index);
			if len(nextIndex) == 0:
				continue;
			nextIndex = nextIndex[0];
			escapePart = value.replace(key, '');
			print(f'EscapePart: {escapePart}';
			while index <= len(string):
				index = nextIndex;
				if index == 0:
					print(f'For index {index} added {escapePart} on start');
					string = escapePart + string;
				else:
					if string[index-1] == escapePart and not passEscaped:
						string = self.__input(string, value, index);
					elif string[index-1] == escapePart and passEscaped:
						pass;
					else:
						string = self.__input(string, value, index);
				nextIndex = self.__indexes(string, key, index);
				if len(nextIndex) == 0:
					break;
				nextIndex = nextIndex[0];
				
		return string;
				"""	
		for i in indexes:
			i = int(i);
			if i == 0:
				print(f'For index {i} added \ on start');
				string = '\\' + string;
				continue;
			text = str(string[i-1] + string[i]);
			if string[i-1] == "\\" and string[i] == '\"':
				print(f' {string[i-1]} {string[i]} is equal to "\\" and "\""');
				print(f'For index {i} passed because of escaped');
				pass;
			else:
				print(f' {string[i-1]} {string[i]} is not equal to "\\" and "\""');
				print(f'For index {i} added \ ');
				string = self.__input(string, '\\\"', i);
		indexes = self.__indexes(string, "'");
		for i in indexes:
			i = int(i);
			if i == 0:
				print(f'For index {i} added \ on start');
				string = '\\' + string;
				continue;
			#text = str(string[i-1] + string[i]);
			print('Indexes of string : ' + ", ".join([string[i] for i in range(len(string))]));
				
			if string[i-1] == "\\" and string[i] == "\'":
				print(f' {string[i-1]} {string[i]} is equal to "\\" and "\'"');
				print(f'For index {i} passed because of escaped');
				pass;
			else:
				print(f' {string[i-1]} {string[i]} is not equal to "\\" and "\'"');
				print(f'For index {i} added \ ');
				string = self.__input(string, "\\\'", i);
		return string;"""
	
	def array(self, array):
		pass;
	
	def dictionary(self, dictionary):
		pass;
	
class Decode():
	def string(self, string):
		string = string.replace('""', '"');
		return string;
	
	
