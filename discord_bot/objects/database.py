import os, psycopg2

from psycopg2.extensions import AsIs

#
# Database connection handle class
#

class DB_conn:
	def __init__(self, table):
		self.table = table
		self.cursor = self.__gen_cursor()
    	
	def __gen_cursor(self):
		connection = os.environ.get('DATABASE_URL')
		con = psycopg2.connect(connection)
		cur = con.cursor()
		return cur
	
	def __revoke_cursor(self):
		# Check somewhere how it was handled by now and GET IT in HERE!
		return False
	
	def add(self, payload):
		cur = self.cursor
		table = self.table
		columns = list(payload.keys())
		values = list(payload.values())
		cur.execute(
			"""
			INSERT INTO %s (%s)
			VALUES (%s);
			""", (table, AsIs(','.join(columns)), tuple(values))
		)
		
	def update(self, condition, payload): 
		cur = self.cursor
		table = self.table
		columns = list(payload.keys())
		values = tuple([payload[column] for column in columns])
		for value in values:
			if isinstance(value, dict):
				values[values.index(value)] = json.dumps(value, indent = 4)  
		cond_key = list(condition.keys())[0]
		condition = list(condition.values())[0]
		cur.execute(
			"""
			UPDATE %s
			SET (%s) = %s
			WHERE %s = %s
			""", (table, tuple(columns), values, cond_key, condition) # AsIs(','.join(columns))
		)
		
	def read(self, condition):
		print("table: " + self.table)
