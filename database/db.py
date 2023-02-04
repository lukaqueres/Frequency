import doctest
import psycopg2
import os

from psycopg2 import sql
from typing import Any


# @link: https://www.psycopg.org/docs/index.html


class Database:
	"""
		Example of usage:

		>>> db = Database(os.environ.get('DATABASE_URL'))

		>>> db.select("guilds",["id", "name"],**{"prefix": "//", "name": "Wierd_'name-test\\""})
		{'id': 2, 'name': 'Wierd_\\'name-test"'}
		>>> db.select("guilds",["name", ],**{"id": 1,})
		{'name': 'Sample_name'}
		>>> db.select("guilds",["name", ], limit = None)
		[{'name': 'Sample_name'}, {'name': 'Wierd_\\'name-test"'}]

		>>> db.insert("guilds", **{"id": 10, "name": "Delete'\\"ted", "prefix": "/"})
		{'id': 10, 'name': 'Delete\\'"ted', 'prefix': '/'}
		"""

	def __init__(self, url: str):
		self.con = psycopg2.connect(url)
		self.cur = self.con.cursor()

	def select(self, table: str, columns: list, limit: None | int = 1, **constraints: dict) -> Any:
		query = "SELECT {columns} FROM {table} {where} {constraints} {limit}"
		data = {}
		cols = [sql.Identifier(c) for c in columns]
		formats = {"columns": sql.SQL(',').join(cols)}
		formats.update(table=sql.Identifier(table))

		if constraints:
			formats.update(where=sql.SQL("WHERE"))
			i = 1
			conditions = {}
			for name, value in constraints.items():
				conditions.update({name: sql.Placeholder(f"constraint{i}{name}v")})
				data.update({f"constraint{i}{name}v": value})
				i += 1
			requisites = sql.SQL(" AND ").join(sql.SQL(" = ").join([sql.Identifier(n), v]) for n, v in conditions.items())
			formats.update(constraints=requisites)
		else:
			formats.update(where=sql.SQL(""), constraints=sql.SQL(""))
			pass
		formats.update(limit=sql.SQL("LIMIT 1" if limit else ""))
		self.cur.execute(sql.SQL(query).format(**formats), data)
		if limit:
			return dict(zip(columns, self.cur.fetchone()))
		else:
			return list(dict(zip(columns, r)) for r in self.cur.fetchall())

	def insert(self, table: str, **values: dict) -> dict:
		query = "INSERT INTO {table} ( {columns} ) VALUES ( {values} )"
		formats = {"table": sql.Identifier(table)}
		formats.update(columns=sql.SQL(", ").join(sql.Identifier(c) for c in values.keys()))
		formats.update(values=sql.SQL(", ").join(sql.Placeholder(f"value{list(values).index(c)}{c}v") for c in values.keys()))
		data = {f"value{list(values).index(n)}{n}v": v for n, v in values.items()}
		self.cur.execute(sql.SQL(query).format(**formats), data)
		return values

	def update(self):
		pass

	def delete(self):
		pass


doctest.run_docstring_examples(Database, globals())
