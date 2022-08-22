import os, psycopg2

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
			""", (table, columns, values)
		)
		
	def update(self, condition, payload): 
		cur = self.cursor
		table = self.table
		columns = list(payload.keys())
		values = list(payload.values()) 
		cur.execute(
			"""
			UPDATE %s
			SET (%s) = (%s)
			WHERE %s = %s
			""", (table, columns, values, list(condition.keys())[0], list(condition.values())[0])
		)
		
	def read(self, condition):
		print("table: " + self.table)
