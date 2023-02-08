import doctest
import psycopg2
import os

from psycopg2 import sql


class Database:
	"""

	@version 0.1.0
	@author lukaqueres

	Example of usage:

	>>> db = Database(os.environ.get('DATABASE_URL'))

	>>> db.select("guilds",["id", "name"],**{"prefix": "//", "name": "Wierd_'name-test\\""})
	{'id': 2, 'name': 'Wierd_\\'name-test"'}
	>>> db.select("guilds",["name", ], limit = None)
	[{'name': 'Sample_name'}, {'name': 'Wierd_\\'name-test"'}]

	>>> db.insert("guilds", **{"id": 10, "name": "Delete'\\"ted", "prefix": "/"})
	{'id': 10, 'name': 'Delete\\'"ted', 'prefix': '/'}
	>>> db.update("guilds", {"name": "Changed\\"me", "prefix": "xd"}, **{"id": 10})
	1
	>>> db.select("guilds",["name", "prefix"],**{"id": 10,})
	{'name': 'Changed"me', 'prefix': 'xd'}
	>>> db.delete("guilds", **{"id": 10})
	1

	@note psycopg2 documentation can be found here U{https://www.psycopg.org/docs/index.html}

	@note In case of transaction error call `con.rollback()`, use of `with` should automatically take care of this

	"""

	def __init__(self, url: str) -> None:
		"""

		@param url: Url used to connect to database in format: `postgresql://username:password@host:5432/table`
		"""
		self.con = psycopg2.connect(url)

	def select(self, table: str, columns: list, limit: None | int = 1, **constraints: dict) -> list | dict:
		"""Selects columns from specified table based on constraints

		@param table: Name of table
		@param columns: Tally of columns to be returned
		@param limit: limit selected rows to number, default 1
		@param constraints: Constraints limiting selection

		@return: Returns list / dict of row(s)
		"""
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
		with self.con.cursor() as curs:
			curs.execute(sql.SQL(query).format(**formats), data)
			if limit == 1:
				return dict(zip(columns, curs.fetchone()))
			else:
				return list(dict(zip(columns, r)) for r in curs.fetchall())

	def insert(self, table: str, **values: dict) -> dict:
		"""Insert row of values to given table

		@param table: Name of table
		@param values: Content of new row
		@return: Passed values
		"""
		query = "INSERT INTO {table} ( {columns} ) VALUES ( {values} )"
		formats = {"table": sql.Identifier(table)}
		formats.update(
			columns=sql.SQL(", ").join(sql.Identifier(c) for c in values.keys()))
		formats.update(
			values=sql.SQL(", ").join(sql.Placeholder(f"value{list(values).index(c)}{c}v") for c in values.keys()))
		data = {f"value{list(values).index(n)}{n}v": v for n, v in values.items()}
		with self.con.cursor() as curs:
			curs.execute(sql.SQL(query).format(**formats), data)
			self.con.commit()
		return values

	def update(self, table: str, values: dict, **constraints: dict) -> int:
		"""Update row(s) values based on constraints

		@param table: Table name
		@param values: New values
		@param constraints: Limit number of affected rows
		@return: Number of affected rows
		"""
		query = "UPDATE {table} SET {values} WHERE {constraints}"
		formats = {"table": sql.Identifier(table)}
		formats.update(
			values=sql.SQL(", ").join(sql.SQL(" = ").join(
					[sql.Identifier(n), sql.Placeholder(f"value{list(values).index(n)}{n}v")]
				) for n, v in values.items()))
		formats.update(
			constraints=sql.SQL(", ").join(sql.SQL(" = ").join(
					[sql.Identifier(n), sql.Placeholder(f"constraint{list(constraints).index(n)}{n}v")]
				) for n, v in constraints.items()))
		data = {f"value{list(values).index(n)}{n}v": v for n, v in values.items()}
		data.update({f"constraint{list(constraints).index(n)}{n}v": v for n, v in constraints.items()})
		with self.con.cursor() as curs:
			curs.execute(sql.SQL(query).format(**formats), data)
			self.con.commit()
			return curs.rowcount

	def delete(self, table: str, **constraints: dict) -> int:
		"""Remove specified records from database

		@param table: Table name
		@param constraints: Limits of deleted rows
		@return: Number of deleted rows
		"""
		query = "DELETE FROM {table} WHERE {constraints}"
		data = {}
		formats = {"table": sql.Identifier(table)}
		if not constraints:
			raise TypeError("Constraints can not be empty")
		i = 1
		conditions = {}
		for name, value in constraints.items():
			conditions.update({name: sql.Placeholder(f"constraint{i}{name}v")})
			data.update({f"constraint{i}{name}v": value})
			i += 1
		requisites = sql.SQL(" AND ").join(sql.SQL(" = ").join([sql.Identifier(n), v]) for n, v in conditions.items())
		formats.update(constraints=requisites)
		with self.con.cursor() as curs:
			curs.execute(sql.SQL(query).format(**formats), data)
			self.con.commit()
			return curs.rowcount


doctest.run_docstring_examples(Database, globals())
