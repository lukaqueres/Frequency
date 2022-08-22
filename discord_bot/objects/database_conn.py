class DB_conn:
	def __init__(self, table):
		self.table = table
    
	def read(self, condition):
		print("table: " + self.table)
