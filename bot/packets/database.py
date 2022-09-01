import os, psycopg2, json, re

# - Import database extensions -
from psycopg2.extensions import AsIs, #quote_ident

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
	def __init__(self):
		super().__init__(); # - Assign Escape and Decode class to handle adapting/decoding of strings, dictionaries etc. to use with dots and better readibility -
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
		print(values);
		values = self.escape.all(values);
		print(values);
		values = self.escape.wrap(values);
		#values = self.adapt.values(values);
		#values = ",".join("'"+ v + "'" if type(v) is str else str(v) for v in values);
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
	
class Escape(Database):
	def __init__(self):
		super().__init__();
		
	def __input(self, s, newstring, index, nofail=False):
		# if index is outside of the string
		if not nofail and index not in range(len(s)):
			return s;
		# if not erroring, but the index is still not in the correct range..
		if index < 0:  # add it to the beginning
			return newstring + s
		if index > len(s):  # add it to the end
			return s + newstring

		# insert the new string between "slices" of the original
		#print(f'Added {newstring} in the middle of {s}');
		return s[:index] + newstring + s[index + 1:]
	
	def __indexes(self, string, lookingFor, start = 0):
		string = string[start:];
		indexes = [i for i, x in enumerate(string, start) if x == lookingFor];
		return indexes;
	
	def __raw(self, string):
		return fr"{string}";
		
	def all(self, values):
		if type(values) is int:
			print('int detected')
			pass;
		elif type(values) is str:
			print('string detected')
			values= self.string(values);
		elif isinstance(values, list):
			print('array detected')
			values = self.array(values);
		elif isinstance(item, dict):
			print('dictionary detected')
			values = self.dictionary(values);
		else:
			print('else detected')
			pass;
		return values;
	
	def string(self, string, passEscaped = True):
		cur = self.cursor;
		print(f'working on string: {string}');
		string = self.__raw(string);
		print(f'working on string: {string}; as raw');
		elements = {'"': "\\\"", "'": '\\\''};
		if True:
			string = quote_ident(string, cur);
			return string;
		for key, value in elements.items():
			#print(f'key: {key}, value: {value}');
			index = 0;
			indexes = self.__indexes(string, key, index);
			print(f'working on string with indexes {indexes} in key {key}');
			if len(indexes) == 0:
				continue;
			nextIndex = indexes[0];
			#print(f'first index: {nextIndex}');
			escapePart = value.replace(key, '');
			#print(f'EscapePart: {escapePart}');
			i = 0;
			while index < len(string) and i in range(len(indexes)):
				#print(f'Podłoga: {i}');
				i += 1;
				index = nextIndex;
				if index == 0:
					#print(f'For index {index} added {escapePart} on start');
					string = escapePart + string;
				else:
					#print(f'Index-1: {string[index-1]} and escape part: {escapePart}');
					if string[index-1] == escapePart and not passEscaped:
						string = self.__input(string, value, index);
					elif string[index-1] == escapePart and passEscaped:
						print(f'working on string with index {index} in key {key} passing it');
						pass;
					else:
						print(f'working on string with index {index} in key {key} adding escape {value}');
						string = self.__input(string, value, index);
				index = index + 1;
				nextIndex = self.__indexes(string, key, index);
				#print(f'Next indexes: {nextIndex} from index {index}');
				if len(nextIndex) == 0:
					break;
				nextIndex = nextIndex[0];
				#print(f'Next index: {nextIndex}');
		print(f'worked on string: {string}; as raw');
		return string;
	
	def array(self, array):
		escapedArray = [];
		for item in array:
			if type(item) is int:
				print('int in array detected')
				pass;
			elif type(item) is str:
				print('string in array detected')
				item = self.string(item);
			elif isinstance(item, list):
				print('array in array detected')
				item = self.array(item);
			elif isinstance(item, dict):
				print('dictionary in array detected')
				item = self.dictionary(item);
			else:
				pass;
			escapedArray.append(item);
		return escapedArray;
		
	
	def dictionary(self, dictionary):
		escapedDictionary = {};
		for key, value in dictionary.items():
			if type(key) is int:
				print('int in dict key detected')
				pass;
			elif type(key) is str:
				print('string in dict key detected')
				key = self.string(key);
			else:
				pass;
			if type(value) is int:
				print('int in dict value detected')
				pass;
			elif type(value) is str:
				print('string in dict value detected')
				value = self.string(value);
			elif isinstance(value, list):
				print('list in dict value detected')
				value = self.array(value);
			elif isinstance(value, dict):
				print('dict in dict value detected')
				value = self.dictionary(value);
			else:
				pass;
			escapedDictionary[key] = value;
		return escapedDictionary;
	
	def wrap(self, values):
		#values = ",".join("'"+ v + "'" if type(v) is str else str(v) for v in values);
		values = ",".join('"'+ v + '"' if type(v) is str else '"' + str(v) + '"' for v in values);
		return values;
	
class Decode():
	def string(self, string):
		string = string.replace('""', '"');
		return string;
	
	
