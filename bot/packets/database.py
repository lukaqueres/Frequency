import os, psycopg2, json

from psycopg2.extensions import AsIs

class Connection:
	def __init__(self):
		self.connection = self.__connect();
		self.cursor = self.__gen_cursor();
		
	def __connect(self):
		connection = os.environ.get('DATABASE_URL');
		con = psycopg2.connect(connection);
		return con;
	
	def __gen_cursor(self):
		con = self.connection;
		cur = con.cursor();
		return cur;
	
	def __revoke_cursor(self):
		# Check somewhere how it was handled by now and GET IT in HERE!
		return False;

class Database(Connection):
	def __init__(self):
		super().__init__()
	
	def add(self, table, payload):
		con = self.connection;
		cur = self.cursor;
		columns = list(payload.keys());
		values = list(payload.values());
		cur.execute(
			"""
			INSERT INTO %s (%s)
			VALUES (%s);
			""", (table, AsIs(','.join(columns)), tuple(values))
		);
		
	def update(self, table, payload, condition): 
		con = self.connection;
		cur = self.cursor;
		columns = list(payload.keys());
		values = [payload[column] for column in columns];
		for value in values:
			if isinstance(value, dict):
				values[values.index(value)] = json.dumps(value, indent = 4);
		values = json.dumps(values, indent = 4)
		cond_key = list(condition.keys())[0];
		condition = list(condition.values())[0];
		cur.execute(
			"""
			UPDATE %s
			SET %s = %s
			WHERE %s = %s
			""", (AsIs(table), AsIs(columns[0] if len(columns) == 1 else tuple(columns)), values, AsIs(cond_key), condition) # AsIs(','.join(columns))
		);
		con.commit();
		
	def read(self, table, condition, columns = ] ):
		con = self.connection;
		cur = self.cursor;
		cond_key = list(condition.keys())[0];
		condition = list(condition.values())[0];
		if len(columns) == 0:
			selector = '*';
		else:
			selector = tuple(columns);
		cur.execute(
			"""
			SELECT %s FROM %s
			WHERE %s = %s
			""", (AsIs(selector), AsIs(table), AsIs(cond_key), condition)
		);
		records = cur.fetchall()
		con.commit()
		if len(records) == 1:
			records = records[0];
			if len(records) == 1:
				records = records[0];
		else:
			r = [];
			for record in records:
				if len(record) == 1:
					r.append(record);
				else:
					r.append(record);
			records = r;
		return records;
	
	
	
	
	
