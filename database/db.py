import doctest
import psycopg2
import os
from typing import Any

# @link: https://www.psycopg.org/docs/index.html


class Database:
	"""
		Example of usage:

		>>> db = Database(os.environ.get('DATABASE_URL'))

		//>>> db.select("example", "my.statement")
		'I like games'
		//>>> print("About: ", db.get("example", "about_this_file"))
		About:  This is a test file for testing config.py file ( Specifically loading JSON values part )
		"""
	def __init__(self, url: str):
		self.con = psycopg2.connect(url)
		self.cur = self.con.cursor()

	def select(self, table: str, columns: str | list, *constraints) -> Any:
		query = "SELECT %(columns)s FROM %(table)s WHERE %(constraints)s"
		data = {'columns': columns, 'table': table, 'constraints': constraints}
		self.cur(query, data)
		return self.cur.fetchall()

	def exists(self):
		pass

	def insert(self, table: str, values: dict) -> dict | bool:
		pass

	def update(self):
		pass

	def delete(self):
		pass


doctest.run_docstring_examples(Database, globals())
